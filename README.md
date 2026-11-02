# Guan Qiang — AI / ML Engineering Portfolio

A project-focused static portfolio for GitHub Pages with readable typography, a blue-gray profile sidebar on wide screens, responsive project panels, expanded project context and contributions, and linked publications. No build step, package installation, database, or API key is required.

## Files

- `index.html`: homepage, five project case studies, expertise, publications, education, and contact.
- `styles.css`: responsive layout, typography, and print styles.
- `resume.html`: printable résumé. Use the page's **Print / Save as PDF** button to export.
- `assets/favicon.svg`: small code-native identity mark.
- `assets/profile.jpg`: the photo supplied in the workspace as `ff4e87c4dc2ee0f6adac14937a991b11.jpg`, copied without modification and displayed beside the name. CSS preserves the original aspect ratio.
- `assets/models/`: eight original SVG system models, reused across all five projects and five publications; every figure can be opened at full size.
- `scripts/build-system-models.py`: standard-library generator for the shared diagram style.
- `docs/system-model-sources.md`: paper figures, method sections, and conceptual-overview provenance for each model.
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

This portfolio targets AI/ML Engineer opportunities. Project text and résumé facts come from the owner's supplied CV. Publication statuses are retained as supplied; the AAAI 2027 submission remains labeled under review even though its arXiv preprint is public. The 2025 journal article title was corrected to the registered title, **Joint Computational Resource Allocation and Layer Partitioning for Federated Learning**, on the homepage and résumé.

At the owner's request, verified paper links are enabled and manuscripts without a public paper link are labeled **Under review / 在投**. Code and Demo placeholders remain noninteractive spans with `role="link"` and `aria-disabled="true"`; they have no `href` and do not enter the keyboard tab order. Quantitative results are labeled To be added, without invented performance numbers. Project cases explain the problem context, supplied contributions, and engineering relevance; publication summaries describe their topics rather than claiming unverified results. Results placeholders share the resource line so that unfinished material stays secondary to the work.

## Paper links

Checked on 2026-11-02 against Crossref publisher metadata, arXiv, and Western University's public faculty publication list. Google Scholar restricts automated access to the supplied profile; the profile itself is linked in the header, publication section, and contact section.

- CRS-Triage: [arXiv:2608.03862](https://arxiv.org/abs/2608.03862). Public preprint; AAAI 2027 submission remains under review.
- Value-Aware Resource Allocation and Layer Partitioning for LLM Inference at the Wireless Edge: no verified public paper URL found; under review as supplied by the owner.
- Personalized Vehicular Health Diagnosis via Large Language Model: [DOI](https://doi.org/10.1109/MCOMSTD.2026.3674904).
- Joint Computational Resource Allocation and Layer Partitioning for Federated Learning: [DOI](https://doi.org/10.1109/JIOT.2025.3592155).
- Security and Efficiency Enhancement for Split Learning: [DOI](https://doi.org/10.1109/PIMRC56721.2023.10293879).

## Responsive layout

Below 900px, the project cases use one column. At 900px and above, the current healthcare project spans the grid and the remaining four projects form two columns. At 1280px and above, the profile becomes a sticky left sidebar and the main content occupies the wider right column. The page expands up to 1540px while keeping paragraph lengths bounded by the project grid. A compact sidebar variant supports wide screens with limited height.

The homepage uses system fonts and plain HTML/CSS, with no JavaScript, external fonts, runtime dependencies, analytics, or tracking. The separate resume page uses a small inline script for its print button.

## Next content pass

Add evidence only after confirming it can be shared publicly:

1. A repository or demo link for each project that has a public artifact.
2. The precise role and scope of contribution for collaborative research.
3. A meaningful result with its evaluation setup, baseline, and limitations.
4. A real screenshot, architecture diagram, or experiment figure where useful.
5. Verified paper links and current publication statuses.

To enable a resource, replace its `<span class="resource-placeholder" role="link" aria-disabled="true">` with a normal `<a href="VERIFIED_URL">` and remove the placeholder title. Each project and publication has its own resource row. Replace a project's results placeholder when real evidence is available. Avoid linking private repositories or clinical data.

Update both `index.html` and `resume.html` when changing shared facts. Dates are written explicitly rather than inferred at runtime.
