#!/usr/bin/env python3
"""Sync publications from Google Scholar (or an exported BibTeX / Semantic Scholar / OpenAlex)
into `_bibliography/papers.bib` while preserving all existing entries and custom al-folio fields.

Usage:
    # Fetch directly from Google Scholar using `scholar_userid` in _config.yml
    python3 bin/sync_scholar.py

    # Preview what would be added without writing any files
    python3 bin/sync_scholar.py --dry-run

    # Merge a BibTeX file exported from Google Scholar (Select all -> Export -> BibTeX)
    python3 bin/sync_scholar.py --from-bib ~/Downloads/citations.bib

    # Fallback sources if Google Scholar rate-limits your network
    python3 bin/sync_scholar.py --source openalex
    python3 bin/sync_scholar.py --source semantic-scholar
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "_config.yml"
DEFAULT_BIB = REPO_ROOT / "_bibliography" / "papers.bib"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


@dataclass
class Paper:
    title: str
    authors: str
    year: str
    venue: str = ""
    url: str = ""
    doi: str = ""
    arxiv: str = ""
    pages: str = ""
    abstract: str = ""
    entry_type: str = "inproceedings"
    raw_bibtex: str | None = None


def read_config_values(config_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not config_path.exists():
        return values
    for line in config_path.read_text(encoding="utf-8").splitlines():
        for key in ("scholar_userid", "first_name", "last_name"):
            m = re.match(rf"^{key}:\s*([^#\n]+)", line)
            if m:
                values[key] = m.group(1).strip().strip("'\"")
    return values


def normalize_title(title: str) -> str:
    cleaned = re.sub(r"[{}]", "", html.unescape(title))
    cleaned = re.sub(r"[^a-z0-9]+", " ", cleaned.lower()).strip()
    return cleaned


def split_bib_entries(bib_text: str) -> tuple[str, list[str]]:
    """Split Jekyll front matter + header from raw BibTeX entries."""
    front_matter = ""
    body = bib_text
    fm_match = re.match(r"\A(---\s*\n.*?\n---\s*\n)", bib_text, flags=re.DOTALL)
    if fm_match:
        front_matter = fm_match.group(1)
        body = bib_text[fm_match.end() :]

    entries: list[str] = []
    i = 0
    n = len(body)
    while i < n:
        at = body.find("@", i)
        if at == -1:
            break
        brace_open = body.find("{", at)
        if brace_open == -1:
            break
        depth = 0
        j = brace_open
        while j < n:
            ch = body[j]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    entries.append(body[at : j + 1].strip())
                    i = j + 1
                    break
            j += 1
        else:
            break
    return front_matter, entries


def extract_bib_field(entry: str, field: str) -> str:
    pattern = re.compile(rf"\b{re.escape(field)}\s*=\s*", re.IGNORECASE)
    m = pattern.search(entry)
    if not m:
        return ""
    pos = m.end()
    n = len(entry)
    if pos >= n:
        return ""
    opener = entry[pos]
    if opener == "{":
        depth = 0
        start = pos + 1
        for i in range(pos, n):
            if entry[i] == "{":
                depth += 1
            elif entry[i] == "}":
                depth -= 1
                if depth == 0:
                    return entry[start:i].strip()
    elif opener == '"':
        start = pos + 1
        i = start
        while i < n:
            if entry[i] == '"' and entry[i - 1] != "\\":
                return entry[start:i].strip()
            i += 1
    else:
        end = re.search(r"[,}\n]", entry[pos:])
        return entry[pos : pos + end.start()].strip() if end else entry[pos:].strip()
    return ""


def extract_bib_key(entry: str) -> str:
    m = re.match(r"@\w+\s*\{\s*([^,\s]+)\s*,", entry)
    return m.group(1) if m else ""


def existing_titles_and_keys(bib_text: str) -> tuple[set[str], set[str]]:
    _, entries = split_bib_entries(bib_text)
    titles: set[str] = set()
    keys: set[str] = set()
    for entry in entries:
        key = extract_bib_key(entry)
        if key:
            keys.add(key.lower())
        title = extract_bib_field(entry, "title")
        if title:
            titles.add(normalize_title(title))
    return titles, keys


def is_duplicate(title: str, existing_titles: set[str]) -> bool:
    norm = normalize_title(title)
    if not norm:
        return True
    if norm in existing_titles:
        return True
    # Treat very close prefix/containment matches (e.g. minor subtitle variation) as duplicates
    for existing in existing_titles:
        if len(norm) >= 25 and len(existing) >= 25:
            if norm in existing or existing in norm:
                return True
    return False


def make_bib_key(paper: Paper, existing_keys: set[str]) -> str:
    first_author = paper.authors.split(" and ")[0].split(",")[0].strip()
    last_word = first_author.split()[-1] if first_author else "paper"
    last_clean = re.sub(r"[^a-z0-9]", "", last_word.lower()) or "paper"
    year = re.sub(r"[^0-9]", "", paper.year) or "nd"
    words = [w for w in re.findall(r"[a-z0-9]+", paper.title.lower()) if len(w) > 2]
    slug = words[0] if words else "work"
    base = f"{last_clean}-{year}-{slug}"
    key = base
    suffix = 2
    while key.lower() in existing_keys:
        key = f"{base}-{suffix}"
        suffix += 1
    existing_keys.add(key.lower())
    return key


def escape_bib_value(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().replace('"', "'")


def format_bibtex(paper: Paper, existing_keys: set[str]) -> str:
    if paper.raw_bibtex:
        entry = paper.raw_bibtex.strip()
        # Ensure `selected = {false},` is present so al-folio handles it cleanly
        if not re.search(r"\bselected\s*=", entry, re.IGNORECASE):
            entry = re.sub(
                r"(@\w+\s*\{[^,]+,\s*\n?)",
                r"\1    selected = {false},\n",
                entry,
                count=1,
            )
        return entry

    key = make_bib_key(paper, existing_keys)
    entry_type = paper.entry_type
    venue_field = "journal" if entry_type == "article" else "booktitle"
    lines = [
        f"@{entry_type}{{{key},",
        "    selected = {false},",
        f'    title = "{escape_bib_value(paper.title)}",',
        f'    author = "{escape_bib_value(paper.authors)}",',
    ]
    if paper.venue:
        lines.append(f'    {venue_field} = "{escape_bib_value(paper.venue)}",')
    if paper.year:
        lines.append(f'    year = "{escape_bib_value(paper.year)}",')
    if paper.pages:
        lines.append(f'    pages = "{escape_bib_value(paper.pages)}",')
    if paper.doi:
        lines.append(f'    doi = "{escape_bib_value(paper.doi)}",')
    if paper.arxiv:
        lines.append(f'    arxiv = "{escape_bib_value(paper.arxiv)}",')
    if paper.url:
        lines.append(f'    url = "{escape_bib_value(paper.url)}",')
    if paper.abstract:
        lines.append(f'    abstract = "{escape_bib_value(paper.abstract)}",')
    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Source 1: Google Scholar profile page (no external dependencies)
# ---------------------------------------------------------------------------


class ScholarProfileParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[dict[str, str]] = []
        self._in_row = False
        self._in_title = False
        self._in_gray = False
        self._gray_index = 0
        self._in_year = False
        self._current: dict[str, str] = {}
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        cls = attr_map.get("class") or ""
        if tag == "tr" and "gsc_a_tr" in cls:
            self._in_row = True
            self._gray_index = 0
            self._current = {"title": "", "href": "", "authors": "", "venue": "", "year": ""}
        elif self._in_row and tag == "a" and "gsc_a_at" in cls:
            self._in_title = True
            self._current["href"] = attr_map.get("href") or ""
            self._buf = []
        elif self._in_row and tag == "div" and "gs_gray" in cls:
            self._in_gray = True
            self._buf = []
        elif self._in_row and tag == "span" and "gsc_a_h" in cls:
            self._in_year = True
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        if self._in_title and tag == "a":
            self._current["title"] = "".join(self._buf).strip()
            self._in_title = False
        elif self._in_gray and tag == "div":
            text = "".join(self._buf).strip()
            if self._gray_index == 0:
                self._current["authors"] = text
            elif self._gray_index == 1:
                self._current["venue"] = text
            self._gray_index += 1
            self._in_gray = False
        elif self._in_year and tag == "span":
            self._current["year"] = "".join(self._buf).strip()
            self._in_year = False
        elif self._in_row and tag == "tr":
            if self._current.get("title"):
                self.rows.append(self._current)
            self._in_row = False

    def handle_data(self, data: str) -> None:
        if self._in_title or self._in_gray or self._in_year:
            self._buf.append(data)


def fetch_url(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_from_google_scholar(user_id: str) -> list[Paper]:
    papers: list[Paper] = []
    cstart = 0
    pagesize = 100
    while True:
        url = (
            f"https://scholar.google.com/citations?user={urllib.parse.quote(user_id)}"
            f"&hl=en&cstart={cstart}&pagesize={pagesize}"
        )
        try:
            page_html = fetch_url(url)
        except urllib.error.HTTPError as err:
            if err.code in (403, 429):
                raise RuntimeError(
                    "Google Scholar rate-limited the request (HTTP "
                    f"{err.code}).\nTry one of:\n"
                    "  1. Export BibTeX from your Google Scholar profile and run:\n"
                    "     python3 bin/sync_scholar.py --from-bib ~/Downloads/citations.bib\n"
                    "  2. Use a public API fallback:\n"
                    "     python3 bin/sync_scholar.py --source openalex"
                ) from err
            raise

        lowered = page_html.lower()
        if "gs_captcha" in lowered or "unusual traffic" in lowered or "recaptcha" in lowered:
            raise RuntimeError(
                "Google Scholar returned a CAPTCHA / anti-bot page.\nTry one of:\n"
                "  1. Export BibTeX from your Google Scholar profile and run:\n"
                "     python3 bin/sync_scholar.py --from-bib ~/Downloads/citations.bib\n"
                "  2. Use a public API fallback:\n"
                "     python3 bin/sync_scholar.py --source openalex"
            )

        parser = ScholarProfileParser()
        parser.feed(page_html)
        if not parser.rows:
            break

        for row in parser.rows:
            authors_raw = row["authors"]
            authors = " and ".join(a.strip() for a in authors_raw.split(",") if a.strip() and a.strip() != "...")
            venue = re.sub(r",?\s*\b(19|20)\d{2}\b\s*$", "", row["venue"]).strip()
            entry_type = "article" if "arxiv" in venue.lower() else "inproceedings"
            arxiv_match = re.search(r"arXiv:(\d{4}\.\d{4,5})", venue, re.IGNORECASE)
            arxiv_id = arxiv_match.group(1) if arxiv_match else ""
            citation_url = (
                f"https://scholar.google.com{row['href']}" if row["href"].startswith("/") else row["href"]
            )
            papers.append(
                Paper(
                    title=row["title"],
                    authors=authors or authors_raw,
                    year=row["year"],
                    venue=venue,
                    url=f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else citation_url,
                    arxiv=arxiv_id,
                    entry_type=entry_type,
                )
            )

        if len(parser.rows) < pagesize:
            break
        cstart += pagesize

    return papers


# ---------------------------------------------------------------------------
# Source 2: Exported BibTeX file (--from-bib)
# ---------------------------------------------------------------------------


def load_from_bib(bib_path: Path) -> list[Paper]:
    text = bib_path.read_text(encoding="utf-8")
    _, entries = split_bib_entries(text)
    papers: list[Paper] = []
    for entry in entries:
        title = extract_bib_field(entry, "title")
        if not title:
            continue
        papers.append(
            Paper(
                title=title,
                authors=extract_bib_field(entry, "author"),
                year=extract_bib_field(entry, "year"),
                venue=extract_bib_field(entry, "booktitle") or extract_bib_field(entry, "journal"),
                raw_bibtex=entry,
            )
        )
    return papers


# ---------------------------------------------------------------------------
# Source 3: OpenAlex API (--source openalex)
# ---------------------------------------------------------------------------


def fetch_from_openalex(author_name: str, author_id: str | None = None) -> list[Paper]:
    if not author_id:
        search_url = (
            "https://api.openalex.org/authors?search="
            + urllib.parse.quote(author_name)
            + "&per-page=5"
        )
        data = json.loads(fetch_url(search_url))
        results = data.get("results", [])
        if not results:
            raise RuntimeError(f"No OpenAlex author found matching '{author_name}'.")
        author_id = results[0]["id"].rsplit("/", 1)[-1]
        print(f"Matched OpenAlex author: {results[0].get('display_name')} ({author_id})")

    works_url = f"https://api.openalex.org/works?filter=author.id:{author_id}&sort=publication_year:desc&per-page=100"
    data = json.loads(fetch_url(works_url))
    papers: list[Paper] = []
    for w in data.get("results", []):
        title = w.get("title") or ""
        if not title:
            continue
        authors = " and ".join(
            a["author"]["display_name"]
            for a in w.get("authorships", [])
            if a.get("author", {}).get("display_name")
        )
        primary_loc = w.get("primary_location") or {}
        source = primary_loc.get("source") or {}
        venue = source.get("display_name") or ""
        doi_raw = w.get("doi") or ""
        doi = re.sub(r"^https?://doi\.org/", "", doi_raw)
        url = primary_loc.get("landing_page_url") or doi_raw
        arxiv = ""
        if "arxiv.org/abs/" in (url or ""):
            arxiv = url.split("arxiv.org/abs/")[-1].split("v")[0]
        papers.append(
            Paper(
                title=title,
                authors=authors,
                year=str(w.get("publication_year") or ""),
                venue=venue,
                doi=doi,
                arxiv=arxiv,
                url=url or "",
                entry_type="article" if w.get("type") == "article" else "inproceedings",
            )
        )
    return papers


# ---------------------------------------------------------------------------
# Source 4: Semantic Scholar API (--source semantic-scholar)
# ---------------------------------------------------------------------------


def fetch_from_semantic_scholar(author_name: str, author_id: str | None = None) -> list[Paper]:
    if not author_id:
        search_url = (
            "https://api.semanticscholar.org/graph/v1/author/search?query="
            + urllib.parse.quote(author_name)
            + "&limit=5&fields=name,affiliations,paperCount"
        )
        data = json.loads(fetch_url(search_url))
        results = data.get("data", [])
        if not results:
            raise RuntimeError(f"No Semantic Scholar author found matching '{author_name}'.")
        author_id = results[0]["authorId"]
        print(f"Matched Semantic Scholar author: {results[0].get('name')} ({author_id})")

    papers_url = (
        f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
        "?fields=title,year,venue,authors,externalIds,url,abstract&limit=100"
    )
    data = json.loads(fetch_url(papers_url))
    papers: list[Paper] = []
    for item in data.get("data", []):
        title = item.get("title") or ""
        if not title:
            continue
        authors = " and ".join(a["name"] for a in item.get("authors", []) if a.get("name"))
        ext = item.get("externalIds") or {}
        doi = ext.get("DOI") or ""
        arxiv = ext.get("ArXiv") or ""
        url = f"https://arxiv.org/abs/{arxiv}" if arxiv else (f"https://doi.org/{doi}" if doi else item.get("url") or "")
        papers.append(
            Paper(
                title=title,
                authors=authors,
                year=str(item.get("year") or ""),
                venue=item.get("venue") or "",
                doi=doi,
                arxiv=arxiv,
                url=url,
                abstract=item.get("abstract") or "",
            )
        )
    return papers


def sort_year_key(paper: Paper) -> int:
    m = re.search(r"\d{4}", paper.year or "")
    return int(m.group(0)) if m else 0


def merge_papers(bib_path: Path, fetched: Iterable[Paper], dry_run: bool = False) -> int:
    bib_text = bib_path.read_text(encoding="utf-8")
    front_matter, existing_entries = split_bib_entries(bib_text)
    existing_titles, existing_keys = existing_titles_and_keys(bib_text)

    new_papers = [p for p in fetched if not is_duplicate(p.title, existing_titles)]
    new_papers.sort(key=sort_year_key, reverse=True)

    if not new_papers:
        print(f"Already up to date! No new papers to add to {bib_path.relative_to(REPO_ROOT)}.")
        return 0

    print(f"Found {len(new_papers)} new paper(s):")
    formatted_new: list[str] = []
    for p in new_papers:
        print(f"  + [{p.year or 'n.d.'}] {p.title}")
        formatted_new.append(format_bibtex(p, existing_keys))
        existing_titles.add(normalize_title(p.title))

    if dry_run:
        print("\n--dry-run enabled; no files were modified.")
        return len(new_papers)

    all_entries = formatted_new + existing_entries
    header = front_matter if front_matter else "---\n---\n"
    updated = header.rstrip("\n") + "\n\n" + "\n\n".join(all_entries) + "\n"
    bib_path.write_text(updated, encoding="utf-8")
    print(f"\nUpdated {bib_path.relative_to(REPO_ROOT)} with {len(new_papers)} new paper(s).")
    print("Tip: Set `selected = {true}`, `abbr = \"...\"`, and `project = {/projects/.../}` on any paper you want to feature.")
    return len(new_papers)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync publications into _bibliography/papers.bib.")
    parser.add_argument(
        "--source",
        choices=("scholar", "openalex", "semantic-scholar"),
        default="scholar",
        help="Metadata source when not using --from-bib (default: scholar).",
    )
    parser.add_argument(
        "--from-bib",
        type=Path,
        help="Path to a BibTeX file exported from Google Scholar (or Zotero/ACL Anthology).",
    )
    parser.add_argument("--user-id", help="Override Google Scholar user ID (default: read from _config.yml).")
    parser.add_argument("--author-id", help="Explicit OpenAlex or Semantic Scholar author ID.")
    parser.add_argument("--bib", type=Path, default=DEFAULT_BIB, help="Path to papers.bib.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Path to _config.yml.")
    parser.add_argument("--dry-run", action="store_true", help="Preview new entries without modifying papers.bib.")
    args = parser.parse_args()

    cfg = read_config_values(args.config)
    author_name = f"{cfg.get('first_name', '')} {cfg.get('last_name', '')}".strip()

    try:
        if args.from_bib:
            fetched = load_from_bib(args.from_bib)
        elif args.source == "scholar":
            user_id = args.user_id or cfg.get("scholar_userid", "")
            if not user_id:
                raise RuntimeError("No `scholar_userid` found in _config.yml. Pass --user-id.")
            fetched = fetch_from_google_scholar(user_id)
        elif args.source == "openalex":
            fetched = fetch_from_openalex(author_name, args.author_id)
        else:
            fetched = fetch_from_semantic_scholar(author_name, args.author_id)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    merge_papers(args.bib, fetched, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
