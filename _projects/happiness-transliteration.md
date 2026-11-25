---
layout: page
title: "Happiness is Sharing a Vocabulary: A Study of Transliteration Methods"
description: EACL 2026 (Main Conference)
img: assets/img/projects/happiness-transliteration_fig1.png
importance: 2
category: research
related_publications: false
---

> **Work in progress:** This project page is currently being updated. In the meantime, you can read the paper on [ACL Anthology](https://aclanthology.org/2026.eacl-long.365/) or view it on [alphaXiv](https://www.alphaxiv.org/overview/2510.10827).

**Authors:** Haeji Jung, Jinju Kim, Kyungjin Kim, Youjeong Roh, David R. Mortensen  
**Venue:** Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2026), Volume 1: Long Papers  
**Links:** [ACL Anthology](https://aclanthology.org/2026.eacl-long.365/) | [arXiv](https://arxiv.org/abs/2510.10827) | [alphaXiv](https://www.alphaxiv.org/overview/2510.10827) | [DOI](https://doi.org/10.18653/v1/2026.eacl-long.365) <!-- | [Code](https://github.com/...) | [Blog Post](/blog/...) -->

---

<div class="row justify-content-sm-center">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/projects/happiness-transliteration_fig1.png" title="Transliteration analysis schema and examples" class="img-fluid rounded z-depth-1" zoomable=true %}
  </div>
</div>
<div class="caption">
  <strong>Figure 1:</strong> Top left: Conceptual visualization of the transliteration analysis schema, positioning input types (Ortho, IPA, Rom, Cipher) based on shared character set, token set, and phonology. Top right: KDE plot showing empirical distribution of overlap ratios for each quantifiable component. Bottom: Transliteration examples generated with each method.
</div>

### Abstract

Transliteration has emerged as a promising means to bridge the gap between various languages in multilingual NLP, showing promising results especially for languages using non-Latin scripts. We investigate the degree to which shared script, overlapping token vocabularies, and shared phonology contribute to performance of multilingual models. To this end, we conduct controlled experiments using three kinds of transliteration (romanization, phonemic transcription, and substitution ciphers) as well as orthography. We evaluate each model on three downstream tasks—named entity recognition (NER), part-of-speech tagging (POS) and natural language inference (NLI)—and find that romanization significantly outperforms other input types in 7 out of 8 evaluation settings, largely consistent with our hypothesis that it is the most effective approach. We further analyze how each factor contributed to the success, and suggest that having longer (subword) tokens shared with pre-trained languages leads to better utilization of the model.

<!--
### Related Blog Post

- Read the related post on my blog: [Post Title](/blog/2026/your-post-slug/)
-->

### Citation

```bibtex
@inproceedings{jung-etal-2026-happiness,
    title = "Happiness is Sharing a Vocabulary: A Study of Transliteration Methods",
    author = "Jung, Haeji and Kim, Jinju and Kim, Kyungjin and Roh, Youjeong and Mortensen, David R.",
    booktitle = "Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = mar,
    year = "2026",
    address = "Rabat, Morocco",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.eacl-long.365/",
    doi = "10.18653/v1/2026.eacl-long.365",
    pages = "7797--7816",
}
```
