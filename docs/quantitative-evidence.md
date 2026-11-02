# Quantitative evidence used in the portfolio

Checked against the owner's four supplied PDFs on 2026-11-02, including visual inspection of result tables and figures. These are paper-reported research results and experimental scope, not independently reproduced outcomes or production guarantees. Individual contribution and shared study outcomes are kept distinct. No unverified "SOTA" claim has been added.

## CRS-Triage

Source: `2608.03862v1.pdf`, Experimental Setup (p. 5), Tables 1–2 (p. 6). Public paper: <https://arxiv.org/abs/2608.03862>.

- Retrospective MIMIC-IV-ED v2.2 study: **418,100 adult encounters**, **201,252 patients**, five acuity classes.
- **70% / 10% / 20% patient-level** train/validation/test split; all encounters of a patient remain in the same subset.
- Reported mean over **five random seeds** at full coverage: **Macro-F1 0.742 ± 0.006**, versus **0.707 ± 0.005** for base evidential fusion. This is the highest Macro-F1 among the eight comparison methods in Table 1; it is not a claim of global or current state of the art.
- Full-coverage under-triage: **13.1% → 9.6%** compared with base evidential fusion, a **3.5 percentage-point** reduction. Over-triage increases **14.5% → 15.1%**; this trade-off remains visible alongside the result.
- At **80% coverage**, accepted-case under-triage is **4.7%** for the CRS confidence score, versus **5.9%** for evidential-certainty selection using the same classifier. This is a selection-method comparison, not a comparison of independently trained classifiers.
- On the healthcare project card, these numbers are explicitly labeled **related first-author research**. They are not silently attributed to production measurements of the Mitacs pipeline.

## Resource-aware federated learning

Source: `Joint_Computational_Resource_Allocation_and_Layer_Partitioning_for_Federated_Learning.pdf`, Table IV and Sec. V-B (pp. 11–12). Public paper: <https://doi.org/10.1109/JIOT.2025.3592155>.

- Table IV uses a **20-layer** model and **5, 10, 20, and 50 clients**. Both proposed methods have **zero energy-depleted clients** in the reported configurations.
- At **50 clients**, **JCRALP: 0**, **AdaptSFL: 14** energy-depleted clients. The website reports the counts and setting rather than implying energy-budget guarantees for arbitrary deployments.
- A separate non-IID CIFAR-10 experiment uses **ResNet-18**, **20 heterogeneous clients**, **100 training rounds**, and four classes per client. The paper reports participation of all **20 clients**, versus **4–16 clients** for the baselines.
- Latency percentage improvements are not fabricated or estimated from plots.

## Split-learning admission security

Source: `Security_and_Efficiency_Enhancement_for_Split_Learning_A_Machine_Learning_based_Malicious_Clients_Detection_Approach.pdf`, Sec. IV-A, Tables II–III, Figs. 3–4 (pp. 5–6). Public paper: <https://doi.org/10.1109/PIMRC56721.2023.10293879>.

- CIC-IDS2017 feature selection retains **50 of 78 features**.
- **11 TVAE models × 10,000 synthetic samples = 110,000 additional minority-attack samples**. This also agrees with the Table II attack-count increase, **666,556 − 556,556 = 110,000**.
- The paper reports **98% binary-classification accuracy** and **AUROC 0.98**.
- Setup: **80% / 20% train/test split**, grid search with **three-fold cross-validation**, a six-hidden-layer classifier, 256 neurons per layer, and 20 epochs.
- The website identifies these as reported benchmark classifier results, not live attack-blocking rates. Precision and F1 claims are not expanded because their averaging definitions are not specified in the provided results paragraph.

## Vehicular LLM diagnosis

Source: `Personalized_Vehicular_Health_Diagnosis_via_Large_Language_Model.pdf`, Prototype Setup (p. 6), Performance Evaluation and Performance Analysis (p. 8). Public paper: <https://doi.org/10.1109/MCOMSTD.2026.3674904>.

- Co-authored study, not a claim of sole ownership of the prototype.
- On-board **Gemma3 1B** on **NVIDIA Jetson Nano**; cloud **LLaMA 30B** on a server with **three RTX 3090 GPUs**.
- EngineFaultDB case study: **three synthetic driver profiles** and **three fault scenarios**. The website does not invent a larger test cohort or imply a full factorial test count.
- Reported end-to-end processing time: **1–2 minutes**, including fault localization, query generation, and solution synthesis, depending on complexity.
- The prototype uses a **local network**. NTN is part of the proposed architecture; the reported runtime is not relabeled as a real satellite-network measurement.

## Projects awaiting measurements

No evaluation files were provided for the mathematical-formula, procurement-automation, or wireless-edge LLM-inference projects. Their result placeholders remain pending. Concrete scope descriptions are retained (three formula-processing tasks, three procurement workflows, and joint allocation/partitioning decisions) without inventing accuracy, latency, or time-saved achievements.
