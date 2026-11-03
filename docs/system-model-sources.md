# System architecture illustrations

The page displays eleven flat editorial illustrations: six CV-based engineering cases and five publications. They were created with the built-in image-generation tool, using the flat healthcare illustration as the style reference. Exact prompts are in `docs/flat-illustration-prompts.json`; current metadata is in `assets/illustrations/flat/manifest.json`. The earlier skeuomorphic images and prompts remain as source history. Direction markers in the federated-learning illustration were removed with a targeted edit so the overview represents bidirectional connections without incorrectly directed arrows.

The illustrations use devices, servers, chips, records, dials, and storage objects as explanatory metaphors. They do not establish actual hardware inventories, measured deployment topology, production clinical use, or an evaluation result. Labels and captions identify the relevant system concepts. The vehicular study's proposed satellite connectivity remains distinct from its measured local-network prototype in the adjacent study text.

Seven precise SVG architectures remain linked where relevant. Existing SVG files use a 1200 × 760 canvas and common typography, modules, arrows, and semantic palette. The new heterogeneous-device inference project has its own illustration, separate from the wireless-edge manuscript's conceptual architecture; their evaluation results are not merged.

The six engineering illustrations use the owner's 2026-11-03 CV: clinical NLP/HPC; two Jetson devices, three Raspberry Pi gateways and a GPU server for inference; heterogeneous LoRA adaptation; two Jetson video endpoints; industrial surface inspection; and Raspberry Pi acquisition with Jetson Nano mathematical OCR. These are explanatory compositions, not deployment photographs or detailed implementation specifications. New standalone SVG schematics have not been asserted for projects without supplied specifications.

The diagrams distinguish devices and server hosts, application or model components, data stores, and deployment or trust boundaries. They are architectural views rather than numbered processing steps. Clinical model internals use a model architecture; projects without full implementation specifications use explicitly conceptual logical architectures. Host placement is shown only where supported by the supplied description or paper.

- Blue: input data, context, or communication.
- Indigo: models and computation.
- Amber: policy, constraints, or admission controls.
- Teal: system decisions and outputs.

Solid blue connections carry data or model traffic. Dashed amber connections carry policy or training signals. Teal connections carry responses or feedback. Server, device, document, network, and database shapes distinguish system entities from internal modules.

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
- Preserved structure: heterogeneous clients retain local data and prefix layers; a central server contains the controller, shared CPU pool, and per-client model tails. Per-client split points and server computational shares are jointly selected. Activations and gradients use distinct connections across the client/server boundary.
- Controller label summarizes the optimization-based method for profiled conditions and modified TD3 for uncertain system parameters. No fixed split positions or measured resource shares are invented.
- Used with the 2025 publication. The separate security research is illustrated in the PIMRC paper, without implying one combined evaluated system.

### Personalized vehicular health diagnosis

- Local reference: `Personalized_Vehicular_Health_Diagnosis_via_Large_Language_Model.pdf`.
- Main source: Fig. 2–3 and Methodology, PDF pp. 3–5; NTN integration is described on p. 5 onward.
- Public reference: <https://doi.org/10.1109/MCOMSTD.2026.3674904>.
- Preserved structure: sensor data and driver profile; lightweight on-board LLM; compact query and NTN connectivity; history-aware query augmentation and RAG retrieval; cloud LLM; personalized warning/action; driver and professional review; curated feedback into the knowledge base.
- Vehicle and cloud hosts enclose their respective components; the network is separate. Query augmentation and retrieval are condensed into one module. Guidance returns to the vehicle, and a separate feedback connection enters expert curation before the knowledge base. The diagram identifies the reported prototype hardware and explicitly distinguishes proposed NTN connectivity from the measured local-network prototype.

### Split-learning security and efficiency

- Local reference: `Security_and_Efficiency_Enhancement_for_Split_Learning_A_Machine_Learning_based_Malicious_Clients_Detection_Approach.pdf`.
- Main source: Fig. 1–2 and Sec. III, PDF pp. 2–4.
- Public reference: <https://doi.org/10.1109/PIMRC56721.2023.10293879>.
- Preserved structure: separate untrusted client, server admission gateway, protected training backend, and offline model-training component. The gateway encloses ML-based risk ranking, risk-adapted Hashcash verification, policy settings, and a temporary blocklist. Correct and timely solutions admit the client; high-risk requests and invalid/late solutions enter the blocklist. Challenge and proof connections are separate.
- Offline training note: CIC-IDS2017, RFE, and TVAE-based augmentation. The detailed Fig. 1 / Sec. III description is followed for risk-score direction: higher maliciousness risk leads to blocking.

## Project-level logical architectures

The remaining diagrams use the owner's supplied project descriptions. Detailed manuscripts or implementation specifications were not available for these cases, so their captions identify them as logical or conceptual architectures. These are explanatory module decompositions, not claims of a verified production topology.

- `healthcare-pipeline.svg`: clinical-input boundary and secure HPC deployment boundary, with clinical-record storage, evidence-quality constraints, preprocessing, feature extraction, risk models, evaluation, and analysis-output storage.
- `edge-llm.svg`: device host, wireless network, edge-server host, and value-aware coordinator for the manuscript under revision. This remains separate from the new CV's deployed heterogeneous-device inference project; the full manuscript was not supplied.
- `formula-recognition.svg`: external document input and editable-LaTeX output around an application boundary containing a localizer, symbol recognizer, two-dimensional structure parser, and serializer. The fraction is an illustrative output-format example.
- `commerce-automation.svg`: legacy procurement schematic from the earlier project description, retained as source history and no longer linked from the homepage after the latest CV update.

## Rebuild

Run `python scripts/build-system-models.py` from the repository. It uses the Python standard library, reads the editable `scripts/system-model-catalog.json`, and writes eight SVG files plus a provenance manifest to `assets/models/`. Labels remain editable as text. Visual review uses local SVG-to-PNG rendering, font-width checks, and XML checks. The website serves SVG files directly and has no rendering-library dependency.
