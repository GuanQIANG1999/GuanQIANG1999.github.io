# Quantitative evidence used in the portfolio

Research-paper results were checked against four supplied PDFs on 2026-11-02, including visual inspection of tables and figures. Engineering-project results were added from the owner's four-page `CV (1).pdf` on 2026-11-03. CV-reported benchmarks are kept separate from paper-reported study outcomes; benchmark code/logs were not supplied for independent reproduction. No unverified global "SOTA" claim has been added.

## CRS-Triage

Source: `2608.03862v1.pdf`, Experimental Setup (p. 5), Tables 1–2 (p. 6). Public paper: <https://arxiv.org/abs/2608.03862>.

- Retrospective MIMIC-IV-ED v2.2 study: **418,100 adult encounters**, **201,252 patients**, five acuity classes.
- **70% / 10% / 20% patient-level** train/validation/test split; all encounters of a patient remain in the same subset.
- Reported mean over **five random seeds** at full coverage: **Macro-F1 0.742 ± 0.006**, versus **0.707 ± 0.005** for base evidential fusion. This is the highest Macro-F1 among the eight comparison methods in Table 1; it is not a claim of global or current state of the art.
- Full-coverage under-triage: **13.1% → 9.6%** compared with base evidential fusion, a **3.5 percentage-point** reduction. Over-triage increases **14.5% → 15.1%**; this trade-off remains visible alongside the result.
- At **80% coverage**, accepted-case under-triage is **4.7%** for the CRS confidence score, versus **5.9%** for evidential-certainty selection using the same classifier. This is a selection-method comparison, not a comparison of independently trained classifiers.
- The CRS-Triage cohort and benchmark now appear only with the publication. The clinical project card instead uses the new CV's separate 12,841-record project evaluation.

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

## CV-reported engineering results (2026-11-03)

Source: owner-supplied `CV (1).pdf`, visually reviewed in full. These numbers are transcribed from the CV, not newly invented or relabeled as independently reproduced research-paper results. The updated CV replaces the previous procurement internship with an industrial computer-vision internship. Code and demo links remain disabled pending actual public artifacts.

### Clinical ML / Mitacs Accelerate (pp. 1–2)

- 12,841 emergency-department records, including 7,924 labeled encounters; three clinical-risk categories.
- Multimodal accuracy 66.3% and Macro-F1 0.628; structured-data XGBoost baseline 57.3% and 0.461.
- Relative Macro-F1 change: `(0.628 - 0.461) / 0.461 = 36.23%`; the page retains the CV's approximately 36% wording.
- 19,323 GAD-7 and 25,757 PHQ-9 assessment records; 901 and 1,481 longitudinal follow-up pairs respectively.
- Reusable NLP components support future transformer/LLM integration; current clinical results are not presented as an already deployed LLM system.

### Heterogeneous-edge LLM inference (p. 2)

- Two NVIDIA Jetson Orin Nano devices, three Raspberry Pi 5 gateways, and a GPU server.
- Benchmark scope: ten concurrent clients and twenty transformer layers.
- P95 TTFT 1.82 → 1.09 s, a 40.1% reduction versus static partitioning; this is not called a 40.1% reduction in total request latency.
- Average throughput 12.6 → 19.4 tokens/s, a 54.0% increase; energy per request reduced by 24.8% as reported in the CV.
- The project hardware benchmark is not attributed to the separate wireless-edge manuscript.

### Edge LoRA fine-tuning (pp. 2–3)

- Peak GPU memory 3.7 → 2.9 GB, down 21.6%.
- Fine-tuning wall time down 24.2% versus fixed-rank LoRA and 10.7% versus HetLoRA.
- Model performance within 0.5 percentage points of the full-precision reference.
- Communication traffic down 31.4% versus conventional federated LoRA.

### Semantic video (p. 3)

- Two Jetson Orin Nano endpoints; two concurrent 256 × 256 streams, approximately 5 FPS and 190 ms processing latency per frame.
- 8:1 compression / 87.5% transmitted-data reduction is compared with uncompressed RGB, not a named video codec.
- Under noisy conditions: PSNR +2.9 dB and SSIM 0.81 → 0.89 versus the CV's conventional-transmission baseline. A channel SNR or codec configuration is not invented.

### Industrial defect detection internship (p. 2)

- Precision **over 93.2%**, recall **over 90.1%**, and processing/inference latency **below 120 ms/image**; inequality bounds are preserved.
- The CV does not identify a detector architecture, compute device, evaluation dataset size, or before/after manual-inspection timing. None is invented.

### Embedded mathematical OCR (p. 3)

- Detection mAP@0.5 94.2%; symbol-recognition accuracy 96.1%; expression exact match 86.5%. These three definitions remain distinct.
- TensorRT/FP16 latency 1.74 → 1.15 s/image, down 33.9%.
- Jetson Nano inference and Raspberry Pi image acquisition. The evaluation dataset size and split are not invented.
