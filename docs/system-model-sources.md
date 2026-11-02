# System model illustrations

Eight original SVG diagrams are used in ten places: all five projects and all five publications. Where a project and publication describe the same research, they share the same asset. Every diagram uses the same canvas, typography, rounded modules, arrow conventions, and semantic palette.

- Blue: input data, context, or communication.
- Indigo: models and computation.
- Amber: policy, constraints, or admission controls.
- Teal: system decisions and outputs.

These are explanatory system schematics, not charts of measured results. The IEEE page images and PDFs were used for local reference only and have not been added to the public repository. The diagrams are redrawn from the described systems rather than copied screenshots of the published figures.

## Paper-based models

### CRS-Triage

- Local reference: `2608.03862v1.pdf`.
- Main source: Fig. 1 and Method, PDF pp. 3–5.
- Public reference: <https://arxiv.org/abs/2608.03862>.
- Preserved structure: structured data plus missingness mask; separate structured/text encoding and evidence heads; modality reliability, evidential uncertainty, and cross-modal consistency; evidential fusion; confidence threshold; predict-or-defer output.
- The training note includes evidential, selective, disagreement, and under-triage penalty objectives. Numerical performance results are not plotted.

### Joint computational resource allocation and layer partitioning

- Local reference: `Joint_Computational_Resource_Allocation_and_Layer_Partitioning_for_Federated_Learning.pdf`.
- Main source: Fig. 1 and Sec. II–IV, especially PDF pp. 3–4 for the system.
- Public reference: <https://doi.org/10.1109/JIOT.2025.3592155>.
- Preserved structure: heterogeneous clients retain local data and prefix layers; server branches run the remaining layers; per-client split points and server computational shares are jointly selected. Activations and gradients cross the partition.
- Controller label summarizes the optimization-based method for profiled conditions and modified TD3 for uncertain system parameters. No fixed split positions or measured resource shares are invented.
- Reused for the distributed-learning project and the 2025 publication. The project's separate security research is illustrated in the PIMRC paper, rather than implying one combined, evaluated system.

### Personalized vehicular health diagnosis

- Local reference: `Personalized_Vehicular_Health_Diagnosis_via_Large_Language_Model.pdf`.
- Main source: Fig. 2–3 and Methodology, PDF pp. 3–5; NTN integration is described on p. 5 onward.
- Public reference: <https://doi.org/10.1109/MCOMSTD.2026.3674904>.
- Preserved structure: sensor data and driver profile; lightweight on-board LLM; compact query and NTN connectivity; history-aware query augmentation and RAG retrieval; cloud LLM; personalized warning/action; driver and professional review; curated feedback into the knowledge base.
- Query augmentation and retrieval are condensed into one stage. The return link is explained in the diagram note. The diagram does not imply that driver feedback is inserted into the knowledge base without expert review.

### Split-learning security and efficiency

- Local reference: `Security_and_Efficiency_Enhancement_for_Split_Learning_A_Machine_Learning_based_Malicious_Clients_Detection_Approach.pdf`.
- Main source: Fig. 1–2 and Sec. III, PDF pp. 2–4.
- Public reference: <https://doi.org/10.1109/PIMRC56721.2023.10293879>.
- Preserved structure: incoming request; ML-based maliciousness probability; low-risk path into risk-adapted Hashcash challenge verification; timely/correct solution admits the client; high-risk requests and invalid/late solutions enter a temporary blocklist.
- Offline training note: CIC-IDS2017, RFE, and TVAE-based augmentation. The detailed Fig. 1 / Sec. III description is followed for risk-score direction: higher maliciousness risk leads to blocking.

## Project-level conceptual workflows

The remaining diagrams use the owner's supplied project descriptions. Detailed manuscripts or implementation specifications were not available for these cases, so their captions identify them as project or conceptual overviews.

- `healthcare-pipeline.svg`: clinical records → preprocessing → multimodal features → risk model → evaluation and analysis outputs, with data quality and secure HPC deployment.
- `edge-llm.svg`: prompt → device-side prefix → wireless intermediate-activation transfer → remaining edge-side model → response, with a value-aware resource/split policy. Reused for the project and the corresponding under-review manuscript. This is a conceptual view, not a claim that the full manuscript was inspected.
- `formula-recognition.svg`: document image → formula localization/extraction → symbol and spatial structure recognition → LaTeX. The fraction is explicitly an illustrative output-format example.
- `commerce-automation.svg`: internal procurement tasks → Java / Spring Boot application ↔ SQL records, supporting quotations, invoicing, and supplier management. It does not specify unverified endpoints, schemas, or deployment services.

## Rebuild

Run `python scripts/build-system-models.py` from the repository. It uses the Python standard library, writes the eight SVG files and a provenance manifest to `assets/models/`, and keeps labels editable as text. Visual review used local SVG-to-PNG rendering, alongside font-width and XML checks. The website serves the SVG files directly and has no rendering-library dependency.
