---
layout: page
title: "Text-driven Prototype Learning for Few-Shot Class-Incremental Learning"
description: ICPR 2024
importance: 5
category: research
related_publications: false
---

> **Work in progress:** This project page is currently being updated. In the meantime, you can check out the [ICPR 2024 proceedings](https://link.springer.com/book/9783031801358#overview).

**Authors:** Seongbeom Park\*, Haeji Jung\*, Daewon Chae, Hyunju Yun, Sungyoon Kim, Suhong Moon, Jinkyu Kim, Seunghyun Park  
**Venue:** 27th International Conference on Pattern Recognition (ICPR 2024)  
**Links:** [Proceedings](https://link.springer.com/book/9783031801358#overview)

---

<!--
Add Figure 1 to `assets/img/projects/text-driven-fscil_fig1.png` and uncomment below:

<div class="row justify-content-sm-center">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/projects/text-driven-fscil_fig1.png" title="Figure 1" class="img-fluid rounded z-depth-1" zoomable=true %}
  </div>
</div>
<div class="caption">
  <strong>Figure 1:</strong> Add caption here.
</div>
-->

### Abstract

Few-shot class-incremental learning (FSCIL) aims to learn generalizable representations with large amounts of initial data and incrementally adapt to new classes with limited data (i.e., few-shot). Recently, prototype-based approaches have shown notably improved performance. However, there still remain challenges — their performances often degrade when newly added classes have high similarity with previously seen classes, causing prototypes to be indistinguishable. In this work, we advocate for leveraging textual semantics to learn class-representative and class-distinguishable prototypes, retaining semantic relations between classes. We utilize angular margin loss to leverage textual semantics effectively, encouraging the model to have intra-class compactness and inter-class discrepancies in the embedding space. Our experiments with three public benchmarks (CUB200, CIFAR100, and miniImageNet) show that our proposed method generally matches or outperforms the current state-of-the-art approaches. To further demonstrate the effectiveness of using texts in the FSCIL task, we newly collect visually descriptive and class-discriminative descriptions built upon two widely-used FSCIL benchmarks: CIFAR100-Text and miniImageNet-Text.

<!-- Add a "Related Blog Post" section here whenever you write a post in _posts/ -->

### Citation

```bibtex
@inproceedings{fscil,
    title = "Text-driven Prototype Learning for Few-Shot Class-Incremental Learning",
    author = "Park, Seongbeom and Jung, Haeji and Chae, Daewon and Yun, Hyunju and Kim, Sungyoon and Moon, Suhong and Kim, Jinkyu and Park, Seunghyun",
    booktitle = "Pattern Recognition -- 27th International Conference, ICPR 2024, Proceedings, Part XXXIII",
    year = "2024",
    publisher = "Springer Cham",
}
```
