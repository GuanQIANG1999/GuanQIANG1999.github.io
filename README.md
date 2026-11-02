# Guan Qiang — AI / ML Engineering Portfolio

A project-focused, accessible static portfolio for GitHub Pages. No build step, package installation, database, or API key is required.

## Files

- `index.html`: homepage, five project case studies, expertise, publications, education, and contact.
- `styles.css`: responsive layouts, visual system, print styles, and reduced-motion support.
- `script.js`: progressive project filtering, email copying, and current navigation state.
- `resume.html`: printable résumé. Use the page's **Print / Save as PDF** button to export.
- `assets/favicon.svg`: small code-native identity mark.
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

This portfolio targets AI/ML Engineer opportunities. Project text and résumé facts come from the owner's supplied CV. Publication statuses are retained as supplied; an AAAI 2027 submission is labeled under review, not accepted.

At the owner's request, visible placeholders are retained for project Code and Demo links, publication Paper and Code links, and project results. Resource placeholders are noninteractive spans with `role="link"` and `aria-disabled="true"`; they have no `href` and do not enter the keyboard tab order. Quantitative results are labeled To be added, without invented performance numbers. The visuals are conceptual pipeline diagrams, not experiment results.

Google Fonts enhances the typography when available; system fonts are defined as fallbacks. The site otherwise has no runtime dependencies, analytics, or tracking.

## Next content pass

Add evidence only after confirming it can be shared publicly:

1. A repository or demo link for each project that has a public artifact.
2. The precise role and scope of contribution for collaborative research.
3. A meaningful result with its evaluation setup, baseline, and limitations.
4. A real screenshot, architecture diagram, or experiment figure where useful.
5. Verified paper links and current publication statuses.

To enable a resource, replace its `<span class="resource-placeholder" role="link" aria-disabled="true">` with a normal `<a class="text-link" href="VERIFIED_URL">` and remove the placeholder title. Each project and publication has its own resource row. Replace the results placeholder inside a project's expanded details when real evidence is available. Avoid linking private repositories or clinical data.

Update both `index.html` and `resume.html` when changing shared facts. Dates are written explicitly rather than inferred at runtime.
