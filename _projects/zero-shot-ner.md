---
layout: page
title: "Zero-Shot Cross-Lingual NER Using Phonemic Representations for Low-Resource Languages"
description: EMNLP 2024 (Main Conference)
img: assets/img/projects/zero-shot-ner_fig1.png
importance: 3
category: research
related_publications: false
---

> **Work in progress:** This project page is currently being updated. In the meantime, you can read the paper on [ACL Anthology](https://aclanthology.org/2024.emnlp-main.753) or view it on [alphaXiv](https://www.alphaxiv.org/overview/2406.16030).

**Authors:** Jimin Sohn\*, Haeji Jung\*, Alex Cheng, Jooeon Kang, Yilin Du, David Mortensen  
**Venue:** Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024)  
**Links:** [ACL Anthology](https://aclanthology.org/2024.emnlp-main.753) | [arXiv](https://arxiv.org/abs/2406.16030) | [alphaXiv](https://www.alphaxiv.org/overview/2406.16030) | [Code](https://github.com/Gabriel819/zeroshot_ner)

---

<div class="row justify-content-sm-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/projects/zero-shot-ner_fig1.png" title="Zero-shot Cross-Lingual NER with IPA phonemes" class="img-fluid rounded z-depth-1" zoomable=true %}
  </div>
</div>
<div class="caption">
  <strong>Figure 1:</strong> Zero-shot Cross-Lingual NER with IPA phonemes.
</div>

### Abstract

Existing zero-shot cross-lingual NER approaches require substantial prior knowledge of the target language, which is impractical for low-resource languages. In this paper, we propose a novel approach to NER using phonemic representation based on the International Phonetic Alphabet (IPA) to bridge the gap between representations of different languages. Our experiments show that our method significantly outperforms baseline models in extremely low-resource languages, with the highest average F1 score (46.38%) and lowest standard deviation (12.67), particularly demonstrating its robustness with non-Latin scripts.

<!-- Add a "Related Blog Post" section here whenever you write a post in _posts/ -->

### Citation

```bibtex
@inproceedings{sohn-etal-2024-zero,
    title = "Zero-Shot Cross-Lingual {NER} Using Phonemic Representations for Low-Resource Languages",
    author = "Sohn, Jimin and Jung, Haeji and Cheng, Alex and Kang, Jooeon and Du, Yilin and Mortensen, David",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.emnlp-main.753",
    pages = "13595--13602",
}
```
