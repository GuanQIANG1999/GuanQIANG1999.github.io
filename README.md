# Guan Qiang — AI / ML Engineering Portfolio

A project-focused static portfolio for GitHub Pages with readable typography, a warm ivory and sage palette, a larger photo in a paper-style frame, flat editorial system illustrations, concrete project contributions, and linked publications. No build step, package installation, database, or API key is required to serve the site.

## Files

- `index.html`: homepage, six CV-based engineering cases, five publications/manuscripts, skills, education, awards, and contact.
- `content/cv-portfolio.json`: current project facts, benchmarks, skills, education, and honors from the owner's 2026-11-03 CV.
- `scripts/update-cv-content.py`: standard-library renderer for CV-based sections and the printable HTML resume; preserves publication evidence separately.
- `styles.css`: responsive layout, typography, and print styles.
- `resume.html`: printable résumé. Use the page's **Print / Save as PDF** button to export.
- `assets/favicon.svg`: black QG lettering on a white background; both pages version the icon URL to refresh browser caches.
- `assets/profile.jpg`: the supplied photo, copied without modification. A larger paper-style frame preserves the entire image and its original aspect ratio.
- `assets/illustrations/flat/`: eleven current flat system illustrations, each at 1536 × 1024, with lazy loading and about 1.4 MiB total. The earlier skeuomorphic images remain in the parent folder as source history and are not displayed.
- `assets/models/`: precise SVG system architectures, retained behind relevant **Technical schematic** links.
- `scripts/prepare-illustrations.py`: optional Pillow-based asset preparation; converts generated originals to WebP and writes the illustration manifest. No website runtime dependency.
- `docs/flat-illustration-prompts.json`: current built-in image-generation and correction prompts; `docs/illustration-prompts.json` records the earlier style.
- `scripts/build-system-models.py`: standard-library generator for the shared diagram style.
- `scripts/system-model-catalog.json`: editable titles, accessible descriptions, and source metadata for each architecture.
- `docs/system-model-sources.md`: paper figures, method sections, and conceptual-overview provenance for each model.
- `docs/quantitative-evidence.md`: verified study metrics, baseline comparisons, experiment settings, and scope limits.
- `.nojekyll`: serves the repository directly as a static website.

## Preview locally

From this directory:

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Open `http://127.0.0.1:4173`. Stop with Ctrl+C.

## GitHub Pages

The intended user-site repository is `GuanQIANG1999/GuanQIANG1999.github.io`.
Under **Settings → Pages**, select **Deploy from a branch**, branch **main**, folder **/ (root)**.
The user site is `https://guanqiang1999.github.io/` once GitHub finishes deploying.

The page works under a project subdirectory too because local assets use relative paths. Update the `og:url` metadata if you move it to a different public address.

## Content decisions

This portfolio targets Machine Learning Engineer and Applied Scientist opportunities. The latest owner-supplied CV, `CV (1).pdf` (2026-11-03), drives the six engineering cases and resume, including clinical NLP, heterogeneous-edge inference, LoRA fine-tuning, semantic video, industrial inspection, and embedded mathematical OCR. It replaces the previous procurement-automation internship description. The CV PDF itself is not published in this repository.

The linked CRS-Triage preprint is retained from the earlier publication material as additional research; it was not included in the latest CV's selected publication list. It remains labeled under review for AAAI 2027. The wireless-edge manuscript is updated to **Under revision** according to the new CV. The 2025 journal article retains its registered title, **Joint Computational Resource Allocation and Layer Partitioning for Federated Learning**, rather than the abbreviated title in the CV.

Verified paper links remain enabled; the manuscript without a public paper link has a noninteractive revision-status label. The 17 Code/Demo placeholders have `role="link"`, `aria-disabled="true"`, and no `href`. Project benchmarks are CV-reported results, while publication benchmarks retain their research-paper sources and conditions. The clinical project now reports its own 12,841 records and multimodal evaluation; the 418,100-encounter CRS-Triage cohort appears only with the paper. See `docs/quantitative-evidence.md` for provenance and scope.

## Paper links

Checked on 2026-11-02 against Crossref publisher metadata, arXiv, and Western University's public faculty publication list. Google Scholar restricts automated access to the supplied profile; the profile itself is linked in the header, publication section, and contact section.

- CRS-Triage: [arXiv:2608.03862](https://arxiv.org/abs/2608.03862). Public preprint; AAAI 2027 submission remains under review.
- Value-Aware Resource Allocation and Layer Partitioning for LLM Inference at the Wireless Edge: no verified public paper URL found; under revision per the 2026-11-03 CV.
- Personalized Vehicular Health Diagnosis via Large Language Model: [DOI](https://doi.org/10.1109/MCOMSTD.2026.3674904).
- Joint Computational Resource Allocation and Layer Partitioning for Federated Learning: [DOI](https://doi.org/10.1109/JIOT.2025.3592155).
- Security and Efficiency Enhancement for Split Learning: [DOI](https://doi.org/10.1109/PIMRC56721.2023.10293879).

## Responsive layout

Project cases use full-width rows so that system illustrations remain readable. At 900px and above, the featured project's problem and contribution descriptions form two columns. At 1280px and above, the profile occupies a 300px left column, increasing to 320px on wider screens. Its photo frame is 232–248px wide. The sidebar scrolls naturally, allowing room for the larger portrait. Below 640px, the photo is above the profile text and its frame is 176–216px wide. The page expands up to 1540px; illustrations are capped at 1000px.

The homepage uses system fonts and plain HTML/CSS, with no JavaScript, external fonts, runtime dependencies, analytics, or tracking. The separate resume page uses a small inline script for its print button.

## Next content pass

Add evidence only after confirming it can be shared publicly:

1. A repository or demo link for each project that has a public artifact.
2. The precise role and scope of contribution for collaborative research.
3. A meaningful result with its evaluation setup, baseline, and limitations.
4. A real screenshot, architecture diagram, or experiment figure where useful.
5. Verified paper links and current publication statuses.

To enable a resource, replace its `<span class="resource-placeholder" role="link" aria-disabled="true">` with a normal `<a href="VERIFIED_URL">` and remove the placeholder title. Each project and publication has its own resource row. Replace a project's results placeholder when real evidence is available. Avoid linking private repositories or clinical data.

Update shared facts in `content/cv-portfolio.json`, then run `python scripts/update-cv-content.py`. Update publication facts in both HTML files. Dates are written explicitly rather than inferred at runtime. To prepare new flat assets, run `python scripts/prepare-illustrations.py LOCAL_INPUTS.json --out assets/illustrations/flat --style flat`; original generated images remain in ignored local preview storage.
