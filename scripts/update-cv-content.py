"""Render CV-based portfolio sections and the printable HTML resume.

No website runtime dependencies. Keeps research-publication metrics and links
separate from the owner-supplied CV's project benchmarks.
"""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'cv-flat-1'
DATA = json.loads((ROOT / 'content/cv-portfolio.json').read_text(encoding='utf-8'))
ART = {m['slug']: m for m in json.loads(
    (ROOT / 'assets/illustrations/flat/manifest.json').read_text(encoding='utf-8'))}


def e(value):
    return escape(str(value), quote=True)


def figure(slug, provenance):
    m = ART[slug]
    schematic = ''
    if m.get('technical_schematic'):
        schematic = (f'<a class="schematic-link" href="{e(m["technical_schematic"])}" '
                     'target="_blank" rel="noopener noreferrer">Technical schematic '
                     '<span aria-hidden="true">&#8599;</span></a>')
    return f'''<figure class="system-model illustrated-model">
            <a class="model-image-link" href="{e(m['file'])}" target="_blank" rel="noopener noreferrer" aria-label="Open {e(m['title'])} system illustration at full size (new tab)"><img src="{e(m['file'])}" alt="{e(m['alt'])}" width="{m['width']}" height="{m['height']}" loading="lazy" decoding="async"></a>
            <figcaption><div class="model-caption-row"><span class="model-label">System illustration</span><span class="model-actions"><a href="{e(m['file'])}" target="_blank" rel="noopener noreferrer">View illustration <span aria-hidden="true">&#8599;</span></a>{schematic}</span></div><p class="model-provenance">{provenance}</p></figcaption>
          </figure>'''


def bullets(items, cls='contributions'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{e(x)}</li>' for x in items) + '</ul>'


def project(p):
    featured = ' project-featured' if p.get('featured') else ''
    org = f'<p class="entry-context">{e(p["organization"])}</p>' if p.get('organization') else ''
    overview = f'<p class="project-overview">{e(p["overview"])}</p>'
    contribution = '<h4>My contribution</h4>' + bullets(p['contributions'])
    if p.get('featured'):
        details = f'<div class="featured-details"><div><h4>The problem</h4>{overview}</div><div>{contribution}</div></div>'
    else:
        details = overview + contribution
    metrics = ''.join(f'<div class="metric-card"><span class="metric-value">{e(v)}</span><span class="metric-label">{e(label)}</span></div>' for v, label in p['metrics'])
    note = f'<p class="project-note">{e(p["note"])}</p>' if p.get('note') else ''
    resources = ''.join(f'<span class="resource-placeholder" role="link" aria-disabled="true" title="{name} link to be added">[{name}]</span>' for name in ['Code', 'Demo'])
    return f'''        <article class="project{featured}" id="{e(p['id'])}">
          <p class="project-kicker">{e(p['kind'])}</p>
          <h3>{e(p['title'])}</h3>
          <p class="entry-context">{e(p['context'])}</p>{org}
          {figure(p['slug'], 'Conceptual system illustration; hardware and component placement are illustrative.')}
          {details}
          <p class="engineering-value"><strong>Engineering relevance.</strong> {e(p['value'])}</p>
          <section class="research-results" data-evidence="cv-{e(p['id'])}" aria-label="Project results and evaluation"><h4>Results &amp; evaluation</h4><div class="metric-grid">{metrics}</div><p class="metric-context">{e(p['metric_context'])}</p></section>
          {note}
          <p class="project-topics"><strong>Focus:</strong> {e(p['topics'])}</p>
          <div class="resource-links" aria-label="Project resources">{resources}</div>
        </article>'''


def skill_rows():
    return ''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k, v in DATA['skills'])


def education():
    return '\n'.join(f'''        <div class="education-entry"><div class="entry-heading"><h3>{e(p['degree'])}</h3><span class="entry-date">{e(p['dates'])}</span></div><p>{e(p['institution'])} &middot; {e(p['location'])}</p><p class="entry-context"><strong>GPA:</strong> {e(p['gpa'])}</p><p class="entry-context"><strong>Relevant coursework:</strong> {e(p['courses'])}.</p></div>''' for p in DATA['education'])


def update_index():
    path = ROOT / 'index.html'
    s = path.read_text(encoding='utf-8')
    s = re.sub(r'(<link rel="stylesheet" href="styles.css\?v=)[^"]+', r'\g<1>' + VERSION, s)
    s = s.replace('<meta name="theme-color" content="#f5f7fb">', '<meta name="theme-color" content="#fbf8f2">')
    intro = DATA['intro']
    intro_html = f'''      <section class="introduction" aria-label="Introduction">
        <p class="intro-label">RESEARCH &amp; ENGINEERING</p>
        <p class="intro-lead">{e(intro['lead'])}</p>
        <p>{e(intro['body'])}</p>
        <p class="opportunity-note"><strong>{e(intro['opportunity'])}</strong> {e(intro['opportunity_detail'])}</p>
      </section>

'''
    s = re.sub(r'      <section class="introduction".*?(?=      <section id="work")', lambda _: intro_html, s, flags=re.S)
    work = '''      <section id="work" aria-labelledby="work-title">
        <h2 id="work-title">Projects &amp; Engineering Experience</h2>
        <p class="section-intro">Clinical ML, efficient LLMs, and embedded vision: selected systems, my contributions, and measured results.</p>
        <div class="project-grid">
''' + '\n\n'.join(project(p) for p in DATA['projects']) + '''
        </div>
      </section>

'''
    s = re.sub(r'      <section id="work".*?(?=      <section id="research")', lambda _: work, s, flags=re.S)
    start, end = s.index('      <section id="research"'), s.index('      <section id="approach"')
    research = s[start:end]

    def replace_figure(match):
        old = match.group(0)
        slug = re.search(r'src="assets/illustrations/(?:flat/)?([a-z-]+)\.webp"', old).group(1)
        provenance = re.search(r'<p class="model-provenance">(.*?)</p>', old).group(1)
        return figure(slug, provenance)

    research = re.sub(r'<figure class="system-model illustrated-model">.*?</figure>', replace_figure, research, flags=re.S)
    research = research.replace('Published work, public preprints, and manuscripts under review.', 'Published work, public preprints, and manuscripts under review or revision.')

    def revise_status(match):
        return (match.group(0).replace('Under review', 'Under revision')
                .replace('&#22312;&#25237;', '&#20462;&#25913;&#20013;')
                .replace('Submitted manuscript under review.', 'Manuscript under revision.'))

    research = re.sub(r'<li><h3>Value-Aware Resource Allocation.*?</li>', revise_status, research, flags=re.S)
    s = s[:start] + research + s[end:]
    skills = f'''      <section id="approach" aria-labelledby="skills-title"><h2 id="skills-title">Technical Skills</h2><p class="section-intro">From data preparation and model development to efficient training, inference, and deployment.</p><dl class="skills-list">{skill_rows()}</dl></section>

'''
    s = re.sub(r'      <section id="approach".*?(?=      <section id="about")', lambda _: skills, s, flags=re.S)
    about = f'''      <section id="about" aria-labelledby="education-title"><h2 id="education-title">Education</h2>
{education()}
      </section>

'''
    s = re.sub(r'      <section id="about".*?(?=      <section aria-labelledby="awards-title")', lambda _: about, s, flags=re.S)
    awards = f'''      <section aria-labelledby="awards-title"><h2 id="awards-title">Honors, Awards &amp; Languages</h2>{bullets(DATA['awards'], 'awards-list')}<p><strong>Languages:</strong> English (Fluent), Mandarin Chinese (Native)</p></section>

'''
    s = re.sub(r'      <section aria-labelledby="awards-title".*?(?=      <section id="contact")', lambda _: awards, s, flags=re.S)
    s = s.replace('I am interested in AI/ML engineering roles involving practical model development, data-to-model pipelines, efficient inference, and ML-enabled software.', 'I am interested in Machine Learning Engineer and Applied Scientist roles involving clinical NLP, computer vision, efficient LLMs, and deployed edge AI systems.')
    path.write_text('\n'.join(line.rstrip() for line in s.splitlines()).rstrip() + '\n', encoding='utf-8')


def resume_entry(p):
    org = ' · ' + p['organization'] if p.get('organization') else ''
    result = '; '.join(f'{v}: {label}' for v, label in p['metrics'])
    note = f'<p>{e(p["note"])}</p>' if p.get('note') else ''
    return f'''<div class="resume-entry" id="resume-{e(p['id'])}"><h3>{e(p['title'])}</h3><time>{e(p['context'] + org)}</time>{bullets(p['contributions'], 'resume-bullets')}<p><strong>Results:</strong> {e(result)}.</p><p>{e(p['metric_context'])}</p>{note}</div>'''


def update_resume():
    path = ROOT / 'resume.html'
    s = path.read_text(encoding='utf-8')
    s = re.sub(r'(<link rel="stylesheet" href="styles.css\?v=)[^"]+', r'\g<1>' + VERSION, s)
    pubs = re.search(r'<ul class="resume-pubs">(.*?)</ul>', s, re.S).group(1)
    pubs = pubs.replace('Under review, IEEE Transactions on Vehicular Technology', 'Under revision, IEEE Transactions on Vehicular Technology')
    professional = [p for p in DATA['projects'] if p['kind'].startswith('Professional')]
    projects = [p for p in DATA['projects'] if not p['kind'].startswith('Professional')]
    skills = ''.join(f'<p><strong>{e(k)}:</strong> {e(v)}</p>' for k, v in DATA['skills'])
    schools = ''.join(f'<div class="resume-entry"><h3>{e(p["degree"])} · {e(p["institution"])}</h3><time>{e(p["dates"])} · {e(p["location"])}</time><p><strong>GPA:</strong> {e(p["gpa"])}</p><p><strong>Relevant coursework:</strong> {e(p["courses"])}.</p></div>' for p in DATA['education'])
    content = f'''<main class="resume-sheet">
    <header class="resume-header"><h1>Guan Qiang</h1><p class="resume-role">Machine Learning Engineer · Applied Scientist · AI Systems Researcher</p><p>PhD Candidate, Electrical and Computer Engineering · Western University</p><p>London, Ontario, Canada · <a href="mailto:gqiang@uwo.ca">gqiang@uwo.ca</a> · <a href="https://github.com/GuanQIANG1999">github.com/GuanQIANG1999</a></p></header>
    <section class="resume-section"><h2>Professional Summary</h2><p>{e(DATA['intro']['body'])}</p></section>
    <section class="resume-section"><h2>Technical Skills</h2>{skills}</section>
    <section class="resume-section"><h2>Professional Experience</h2>{''.join(resume_entry(p) for p in professional)}</section>
    <section class="resume-section"><h2>Selected Machine Learning &amp; Engineering Projects</h2>{''.join(resume_entry(p) for p in projects)}</section>
    <section class="resume-section"><h2>Publications &amp; Manuscripts</h2><ul class="resume-pubs">{pubs}</ul></section>
    <section class="resume-section"><h2>Education</h2>{schools}</section>
    <section class="resume-section"><h2>Honors, Awards &amp; Competitions</h2>{bullets(DATA['awards'], 'resume-awards')}</section>
    <section class="resume-section"><h2>Languages</h2><p>English (Fluent) · Mandarin Chinese (Native)</p></section>
    <p class="resume-note">Use “Print / Save as PDF” above to export this résumé.</p>
  </main>'''
    s = re.sub(r'<main class="resume-sheet">.*?</main>', lambda _: content, s, flags=re.S)
    path.write_text('\n'.join(line.rstrip() for line in s.splitlines()).rstrip() + '\n', encoding='utf-8')


if __name__ == '__main__':
    update_index()
    update_resume()
    print('Updated six CV-based cases, five publications, skills, education, awards, and resume.')
