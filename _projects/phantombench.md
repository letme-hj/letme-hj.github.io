---
layout: page
title: "PhantomBench: Benchmarking the Non-existential Threat of Language Models"
description: arXiv Preprint · Shorter version at AIMS Workshop @ COLM 2026
img: assets/img/projects/phantombench_fig1.png
importance: 1
category: research
related_publications: false
---

> **Work in progress:** This project page is currently being updated. In the meantime, you can check out the [full paper on arXiv](https://arxiv.org/abs/2606.11105), the [alphaXiv page](https://www.alphaxiv.org/overview/2606.11105), or the [workshop version on OpenReview](https://openreview.net/forum?id=k6GjJYENrT).

**Authors:** Haeji Jung, Hila Gonen  
**Preprint:** arXiv:2606.11105 (June 2026)  
**Workshop:** Shorter version presented at the First Workshop in AI Measurement Science: Toward Rigorous AI Evaluation (AIMS @ COLM 2026)  
**Links:** [Full Paper (arXiv)](https://arxiv.org/abs/2606.11105) | [alphaXiv](https://www.alphaxiv.org/overview/2606.11105) | [Workshop Version (OpenReview)](https://openreview.net/forum?id=k6GjJYENrT)

---

<div class="row justify-content-sm-center">
  <div class="col-sm-12 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/projects/phantombench_fig1.png" title="PhantomBench pipeline" class="img-fluid rounded z-depth-1" zoomable=true %}
  </div>
</div>
<div class="caption">
  <strong>Figure 1:</strong> The pipeline to construct PhantomBench. Existing concepts from seed terms and entities are decomposed into smaller components (words and n-grams) which are then recombined to form new concepts. A frequency filter discards concepts found in a large corpus, considering concepts with zero matches as non-existent. The resulting concepts are queried through diverse prompts targeting different attributes of the concept. At the bottom is an example response from Gemma 3-12B to a generated non-existent entity, <em>Methods in Intelligent Human</em>.
</div>

### Abstract

Hallucinations, where language models (LMs) generate factually ungrounded responses, pose serious risks, as users tend to blindly rely on them. This is particularly concerning in high-stakes domains, where consequences of such model behavior can lead to significant harms. Despite notable progress in understanding hallucinations, it remains unclear how reliably these models can recognize the limits of their knowledge. We introduce PHANTOMBENCH, the first large-scale benchmark of its kind, comprising more than 60K non-existent terms and entities derived from real concepts across diverse domains. Using our benchmark, we evaluate a total of 21 models of various types and sizes. We show staggering hallucination rates across the board (with average rates as high as 86.7% in some cases), and note that even frontier models surprisingly fail to abstain on non-existent concepts, especially when the input presumes their existence. We then show that PHANTOMBENCH can serve as a proxy for studying model behavior on rare concepts for which models are more prone to hallucinate. We also provide a pipeline to construct PHANTOMBENCH, enabling scalable generation of non-existent concepts tailored to the specific needs of researchers and practitioners.

<!-- Add a "Related Blog Post" section here whenever you write a post in _posts/ -->

### Citation

```bibtex
@article{jung2026phantombench,
    title = "PhantomBench: Benchmarking the Non-existential Threat of Language Models",
    author = "Jung, Haeji and Gonen, Hila",
    journal = "arXiv preprint arXiv:2606.11105",
    year = "2026",
    url = "https://arxiv.org/abs/2606.11105",
}
```
