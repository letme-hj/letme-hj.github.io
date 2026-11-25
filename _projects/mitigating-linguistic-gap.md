---
layout: page
title: "Mitigating the Linguistic Gap with Phonemic Representations for Robust Cross-lingual Transfer"
description: MRL Workshop @ EMNLP 2024
img: assets/img/projects/mitigating-linguistic-gap_fig1.png
importance: 4
category: research
related_publications: false
---

> **Work in progress:** This project page is currently being updated. In the meantime, you can read the paper on [ACL Anthology](https://aclanthology.org/2024.mrl-1.16) or view it on [alphaXiv](https://www.alphaxiv.org/overview/2402.14279).

**Authors:** Haeji Jung, Changdae Oh, Jooeon Kang, Jimin Sohn, Kyungwoo Song, Jinkyu Kim, David Mortensen  
**Venue:** Proceedings of the Fourth Workshop on Multilingual Representation Learning (MRL 2024), co-located with EMNLP 2024  
**Links:** [ACL Anthology](https://aclanthology.org/2024.mrl-1.16) | [arXiv](https://arxiv.org/abs/2402.14279) | [alphaXiv](https://www.alphaxiv.org/overview/2402.14279) <!-- | [Code](https://github.com/...) | [Blog Post](/blog/...) -->

---

<div class="row justify-content-sm-center">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/projects/mitigating-linguistic-gap_fig1.png" title="Orthographic vs. phonemic input representations" class="img-fluid rounded z-depth-1" zoomable=true %}
  </div>
</div>
<div class="caption">
  <strong>Figure 1:</strong> Example of orthographic and phonemic input representations of a sentence (English and Korean).
</div>

### Abstract

Approaches to improving multilingual language understanding often struggle with significant performance gaps between high-resource and low-resource languages. While there are efforts to align the languages in a single latent space to mitigate such gaps, how different input-level representations influence such gaps has not been investigated, particularly with phonemic inputs. We hypothesize that the performance gaps are affected by representation discrepancies between those languages, and revisit the use of phonemic representations as a means to mitigate these discrepancies. To demonstrate the effectiveness of phonemic representations, we present experiments on three representative cross-lingual tasks on 12 languages in total. The results show that phonemic representations exhibit higher similarities between languages compared to orthographic representations, and it consistently outperforms grapheme-based baseline models on languages that are relatively low-resourced. We present quantitative evidence from three cross-lingual tasks that demonstrate the effectiveness of phonemic representations, and it is further justified by a theoretical analysis of the cross-lingual performance gap.

<!--
### Related Blog Post

- Read the related post on my blog: [Post Title](/blog/...)
-->

### Citation

```bibtex
@inproceedings{jung-etal-2024-mitigating,
    title = "Mitigating the Linguistic Gap with Phonemic Representations for Robust Cross-lingual Transfer",
    author = "Jung, Haeji and Oh, Changdae and Kang, Jooeon and Sohn, Jimin and Song, Kyungwoo and Kim, Jinkyu and Mortensen, David",
    booktitle = "Proceedings of the Fourth Workshop on Multilingual Representation Learning (MRL 2024)",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.mrl-1.16",
    pages = "200--211",
}
```
