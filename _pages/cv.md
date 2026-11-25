---
layout: page
permalink: /cv/
title: cv
nav: true
nav_order: 2
cv_pdf: cv.pdf
description:
---

{% assign pdf_url = page.cv_pdf | prepend: '/assets/pdf/' | relative_url %}

<div class="mb-3">
  <a href="{{ pdf_url }}" target="_blank" rel="noopener noreferrer" class="btn btn-sm z-depth-0" role="button">
    <i class="fa-solid fa-file-pdf"></i> Open PDF
  </a>
  <a href="{{ pdf_url }}" download class="btn btn-sm z-depth-0" role="button">
    <i class="fa-solid fa-download"></i> Download CV
  </a>
</div>

<div class="cv-pdf-viewer">
  <object
    data="{{ pdf_url }}"
    type="application/pdf"
    width="100%"
    style="height: 85vh; min-height: 700px; border: 1px solid var(--global-divider-color); border-radius: 6px;"
  >
    <p>
      Your browser does not support inline PDF viewing.
      <a href="{{ pdf_url }}" target="_blank" rel="noopener noreferrer">Click here to view or download my CV (PDF)</a>.
    </p>
  </object>
</div>
