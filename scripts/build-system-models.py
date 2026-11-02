"""Build the portfolio's original, editable SVG system-model illustrations.

No image-generation API or external runtime dependency is required. All diagrams
share typography, colors, node shapes, arrow conventions, and a 1000 x 600 canvas.
Source provenance is recorded in docs/system-model-sources.md and the manifest.
"""

from html import escape
from pathlib import Path
import json
import math
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "models"
W, H = 1000, 600
COLORS = {
    "data": ("#edf4fc", "#b9cfe5", "#365d7f"),
    "model": ("#f0f1fb", "#c9cee8", "#4e5f85"),
    "control": ("#fff5e6", "#e6d0ac", "#896638"),
    "output": ("#eaf6f1", "#b6d9ca", "#397663"),
}


def wrap(text, width, font=24):
    """Conservative wrapping for short, deliberately edited diagram labels."""
    return textwrap.wrap(text, max(8, int(width / (font * .54))),
                         break_long_words=False, break_on_hyphens=False)


class Diagram:
    def __init__(self, slug, title, subtitle, description, source_type, sources):
        self.slug = slug
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.source_type = source_type
        self.sources = sources
        self.back = []
        self.edges = []
        self.front = []
        self.text_checks = []

    def text(self, x, y, text, size=22, color="#3e5670", weight=400,
             anchor="start", layer="front", family="Arial, Helvetica, sans-serif"):
        getattr(self, layer).append(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(text)}</text>')

    def node(self, x, y, w, h, title, sub="", kind="model"):
        assert 20 <= x < W and y >= 105 and x+w <= W-20 and y+h <= 540
        fill, stroke, ink = COLORS[kind]
        self.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                          f'rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        titles = title if isinstance(title, list) else wrap(title, w-24, 24)
        subs = sub if isinstance(sub, list) else (wrap(sub, w-26, 19) if sub else [])
        total = len(titles)*28 + len(subs)*23 + (8 if subs else 0)
        assert total <= h-12, (self.slug, title, total, h)
        baseline = y + (h-total)/2 + 23
        for line in titles:
            self.text(x+w/2, round(baseline, 1), line, 24, ink, 600, "middle")
            self.text_checks.append((line, w-20, 24))
            baseline += 28
        if subs:
            baseline += 5
        for line in subs:
            self.text(x+w/2, round(baseline, 1), line, 19, "#61758a", 400, "middle")
            self.text_checks.append((line, w-20, 19))
            baseline += 23

    def edge(self, points, dashed=False, color="#7891aa", label=None, at=None):
        if dashed:
            segments = []
            for (x1,y1),(x2,y2) in zip(points,points[1:]):
                length=math.hypot(x2-x1,y2-y1)
                if not length: continue
                ux,uy=(x2-x1)/length,(y2-y1)/length
                for distance in range(0,math.ceil(length),13):
                    stop=min(distance+7,length)
                    segments.append(f'M {x1+ux*distance:.1f} {y1+uy*distance:.1f} L {x1+ux*stop:.1f} {y1+uy*stop:.1f}')
            path=' '.join(segments)
        else:
            path = "M " + " L ".join(f"{x} {y}" for x, y in points)
        self.edges.append(f'<path d="{path}" fill="none" stroke="{color}" '
                          'stroke-width="2.6" stroke-linejoin="round"/>')
        (x1,y1),(x2,y2)=points[-2:]
        length=math.hypot(x2-x1,y2-y1)
        ux,uy=(x2-x1)/length,(y2-y1)/length
        tx,ty=x2-ux*2,y2-uy*2
        bx,by=tx-ux*10,ty-uy*10
        self.edges.append(f'<polygon points="{tx:.1f},{ty:.1f} {bx-uy*5:.1f},{by+ux*5:.1f} '
                          f'{bx+uy*5:.1f},{by-ux*5:.1f}" fill="{color}"/>')
        if label:
            assert at
            width = len(label)*9.6+14
            self.front.append(f'<rect x="{at[0]-width/2}" y="{at[1]-18}" width="{width}" '
                              'height="25" rx="5" fill="#f8fafc"/>')
            self.text(*at, label, 18, "#657b91", anchor="middle")

    def lane(self, x, y, w, h, label):
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" '
                         'fill="#f7f9fc" stroke="#d5dfe9" stroke-width="1.5" stroke-dasharray="6 5"/>')
        self.text(x+16, y+26, label, 17, "#798da2", 600, layer="back")

    def note(self, text):
        lines = wrap(text, 922, 18)
        assert len(lines) <= 2, (self.slug, lines)
        for i, line in enumerate(lines):
            self.text(38, 525+i*22, line, 18, "#718298")

    def save(self):
        self.front.insert(0, '<path d="M 30 91 H 970" stroke="#dfe6ee" stroke-width="1.5"/>')
        self.text(32, 42, self.title, 28, "#29445e", 600)
        self.text(33, 72, self.subtitle, 19, "#74869a")
        legend = []
        for x, (kind, label) in zip([36, 235, 442, 653],
                                  [("data", "Data / context"), ("model", "Model / compute"),
                                   ("control", "Policy / control"), ("output", "Decision / output")]):
            fill, stroke, _ = COLORS[kind]
            legend.append(f'<rect x="{x}" y="570" width="16" height="16" rx="4" '
                          f'fill="{fill}" stroke="{stroke}"/>')
            legend.append(f'<text x="{x+25}" y="584" font-family="Arial, Helvetica, sans-serif" '
                          f'font-size="17" fill="#78899d">{label}</text>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
               f'width="{W}" height="{H}" role="img" aria-labelledby="title desc">'
               f'<title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.description)}</desc>'
               '<defs><marker id="arrow" viewBox="0 0 12 12" refX="10" refY="6" '
               'markerWidth="11" markerHeight="11" markerUnits="userSpaceOnUse" orient="auto">'
               '<path d="M 1 1 L 11 6 L 1 11 Z" fill="#7891aa"/></marker></defs>'
               '<rect x="1" y="1" width="998" height="598" rx="18" fill="#f8fafc" stroke="#e0e7ef"/>'
               + ''.join(self.back + self.edges + self.front + legend) + '</svg>')
        path = OUT / f"{self.slug}.svg"
        path.write_text(svg, encoding="utf-8")
        return {"slug": self.slug, "title": self.title, "description": self.description,
                "width": W, "height": H, "source_type": self.source_type,
                "sources": self.sources, "text_checks": self.text_checks}


def healthcare():
    d = Diagram("healthcare-pipeline", "Healthcare ML pipeline", "Project workflow | secure HPC environment",
                "Clinical records enter preprocessing, multimodal feature extraction, and risk prediction. "
                "Model evaluation produces analysis outputs. Data quality informs preprocessing. Processing runs in a secure HPC environment.",
                "project-description", ["Owner-supplied Mitacs project description"])
    d.lane(258, 119, 724, 385, "SECURE HPC PIPELINE")
    d.node(30, 171, 205, 126, "Clinical records", ["Multimodal evidence"], "data")
    d.node(275, 171, 205, 126, "Preprocessing", ["Missing data +", "class imbalance"], "model")
    d.node(520, 171, 205, 126, ["Multimodal", "features"], ["Available evidence"], "model")
    d.node(765, 171, 205, 126, "Risk prediction", ["Clinical risk models"], "model")
    d.node(765, 371, 205, 116, "Evaluation", ["Model performance"], "model")
    d.node(520, 371, 205, 116, "Analysis outputs", ["Model outputs"], "output")
    d.node(275, 371, 205, 116, "Data quality", ["Availability + balance"], "control")
    for a,b in [(235,275),(480,520),(725,765)]: d.edge([(a,234),(b,234)])
    d.edge([(867,297),(867,371)])
    d.edge([(765,429),(725,429)])
    d.edge([(377,371),(377,297)], dashed=True)
    d.note("Project-level workflow: clinical data processing, modeling, evaluation, and a secure deployment boundary.")
    return d


def edge_llm():
    d = Diagram("edge-llm", "LLM inference at the wireless edge", "Conceptual view | layer partitioning + resource allocation",
                "A prompt is processed by prefix layers on a device, intermediate activations pass over a wireless link, "
                "and remaining layers execute at the edge. A value-aware policy controls the split point and computing/communication resources.",
                "project-description", ["Owner-supplied LLM inference project and manuscript description; full manuscript not supplied"])
    d.node(30, 174, 220, 140, "Device", ["LLM prefix layers"], "model")
    d.node(390, 174, 220, 140, "Wireless link", ["Intermediate", "activations"], "data")
    d.node(750, 174, 220, 140, "Wireless edge", ["Remaining LLM layers"], "model")
    d.node(30, 385, 220, 112, "Inference request", ["Prompt"], "data")
    d.node(350, 385, 300, 112, "Value-aware policy", ["Resources + split point"], "control")
    d.node(750, 385, 220, 112, "LLM response", ["Generated output"], "output")
    d.edge([(250,244),(390,244)])
    d.edge([(610,244),(750,244)])
    d.edge([(140,385),(140,314)])
    d.edge([(860,314),(860,385)])
    d.edge([(500,385),(500,314)], dashed=True)
    d.edge([(350,441),(300,441),(300,284),(250,284)], dashed=True)
    d.edge([(650,441),(700,441),(700,284),(750,284)], dashed=True)
    d.note("Conceptual overview of value-aware split inference; the submitted manuscript remains under review.")
    return d


def allocation():
    d = Diagram("federated-partitioning", "Resource-aware federated learning", "JCRALP | per-client layer splits and server CPU allocation",
                "A JCRALP controller selects each client's layer partition and server CPU share. Heterogeneous clients retain local data "
                "and prefix layers, while corresponding server branches process remaining layers. Activations and gradients cross the split.",
                "paper", ["Joint Computational Resource Allocation and Layer Partitioning for Federated Learning, Fig. 1; Sec. II-IV, PDF pp. 3-10"])
    d.node(290, 110, 420, 116, "JCRALP controller", ["Split points + server CPU shares", "Optimization / modified TD3"], "control")
    d.lane(28, 252, 944, 144, "SERVER")
    for x, name, suffix in [(46,"1","1"),(370,"2","2"),(694,"N","N")]:
        cx=x+130
        d.node(x, 287, 260, 96, f"Server branch {name}", [f"Layers s{suffix}+1 .. L", f"CPU share f{suffix}"], "model")
        d.node(x, 431, 260, 104, f"Client {name}", [f"Local layers 1 .. s{suffix}", "Private local data"], "data")
        d.edge([(cx-12,431),(cx-12,383)])
        d.edge([(cx+12,383),(cx+12,431)], dashed=True)
        d.edge([(500,226),(500,239),(cx,239),(cx,287)], dashed=True)
    d.text(500, 558, "Solid: activations | Dashed: gradients or control", 17, "#74889d", anchor="middle")
    return d


def formula():
    d = Diagram("formula-recognition", "Mathematical formula recognition", "Project workflow | document image to editable LaTeX",
                "Document images pass through formula detection and extraction, symbol and spatial-structure recognition, "
                "and conversion to editable LaTeX. An explicitly illustrative fraction conversion is shown below the workflow.",
                "project-description", ["Owner-supplied undergraduate innovation project description"])
    for x, title, sub, kind in [(30,"Document image","Visual math content","data"),
                                (275,"Formula detection","Extract math regions","model"),
                                (520,"Structure recognition",["Symbols + spatial", "relationships"],"model"),
                                (765,"LaTeX output","Editable expression","output")]:
        d.node(x, 171, 205, 136, title, sub, kind)
    for a,b in [(235,275),(480,520),(725,765)]: d.edge([(a,239),(b,239)])
    d.back.append('<rect x="275" y="360" width="450" height="145" rx="16" fill="white" stroke="#d9e3ed"/>')
    d.text(500,390,"Illustrative conversion",19,"#75899e",anchor="middle")
    d.text(378,430,"a",31,"#3d5672",anchor="middle",family="Georgia, serif")
    d.front.append('<path d="M 359 439 H 397" stroke="#3d5672" stroke-width="2"/>')
    d.text(378,477,"b",31,"#3d5672",anchor="middle",family="Georgia, serif")
    d.edge([(432,446),(493,446)])
    d.text(602,454,r"\frac{a}{b}",30,"#397663",anchor="middle",family="Consolas, monospace")
    d.note("Illustrative example: converting a visual mathematical fraction into an editable LaTeX expression.")
    return d


def commerce():
    d = Diagram("commerce-automation", "Enterprise procurement automation", "Project workflow | Java + Spring Boot + SQL",
                "Internal procurement users interact with a Java/Spring Boot application connected to a SQL data store. "
                "The application supports quotations, invoicing, and supplier management. This is a conceptual workflow rather than a detailed implementation specification.",
                "project-description", ["Owner-supplied NS Solutions project description"])
    d.node(30,170,220,126,"Internal users",["Procurement tasks"],"data")
    d.node(355,170,290,126,"Spring Boot app",["Java business logic"],"model")
    d.node(750,170,220,126,"SQL data store",["Business records"],"data")
    d.edge([(250,233),(355,233)])
    d.edge([(645,221),(750,221)])
    d.edge([(750,252),(645,252)],dashed=True)
    for x,title,sub in [(30,"Quotations","Quotation workflows"),(370,"Invoicing","Invoice workflows"),(710,"Suppliers","Supplier management")]:
        d.node(x,389,260,114,title,[sub],"output")
        d.edge([(500,296),(500,342),(x+130,342),(x+130,389)])
    d.note("Conceptual application workflow connecting procurement tasks with Java services and SQL records.")
    return d


def crs():
    d = Diagram("crs-triage", "CRS-Triage", "Reliability-aware evidence fusion and selective prediction",
                "Structured clinical values with a missingness mask and clinical text enter separate encoders and evidence heads. "
                "Modality reliability, uncertainty, and cross-modal consistency guide evidential fusion and class probabilities. A confidence score is compared with a threshold: "
                "predict acuity for sufficiently confident cases or defer the case for assessment. Under-triage receives a larger training penalty.",
                "paper", ["CRS-Triage, Fig. 1 and Method, PDF pp. 3-5"])
    d.node(30,150,205,132,["Structured data"],["Clinical values +", "missingness mask"],"data")
    d.node(30,351,205,132,"Clinical text",["Clinical notes"],"data")
    d.node(275,150,205,132,["Structured", "encoder + head"],["Evidence +", "uncertainty"],"model")
    d.node(275,351,205,132,["Text encoder", "evidence head"],["Evidence +", "uncertainty"],"model")
    d.node(530,233,195,154,["Evidence", "fusion"],["Modality reliability", "Cross-modal", "consistency"],"model")
    d.node(530,116,195,94,["Class", "probabilities"],kind="output")
    d.node(770,246,200,128,"Confidence gate",["Compare s with tau"],"control")
    d.node(770,116,200,94,["Predict acuity"],["s >= tau"],"output")
    d.node(770,416,200,94,"Defer case",["s < tau"],"output")
    d.edge([(235,216),(275,216)])
    d.edge([(235,417),(275,417)])
    d.edge([(480,216),(505,216),(505,280),(530,280)])
    d.edge([(480,417),(505,417),(505,341),(530,341)])
    d.edge([(725,310),(770,310)])
    d.edge([(627,233),(627,210)])
    d.edge([(870,246),(870,210)])
    d.edge([(870,374),(870,416)])
    d.note("Training jointly considers evidential learning, selective prediction, disagreement, and under-triage penalties.")
    return d


def vehicular():
    d = Diagram("vehicular-llm", "Personalized vehicular health diagnosis", "LLM-OBD | on-board query generation, RAG, and feedback",
                "Vehicle sensor data and driver profiles feed an on-board lightweight LLM. A compact query traverses an NTN connection to "
                "server-side query augmentation and knowledge retrieval, then a cloud LLM produces personalized guidance. The action module conveys warnings. "
                "Driver and expert review curate feedback into the knowledge base for future retrieval.",
                "paper", ["Personalized Vehicular Health Diagnosis via Large Language Model, Fig. 2-3 and Methodology, PDF pp. 3-5"])
    top=[(30,"Vehicle data",["Sensors + driver", "profile"],"data"),
         (275,"On-board LLM",["Compact query"],"model"),
         (520,"NTN relay",["Satellite connectivity"],"data"),
         (765,"Query augmentation",["History-aware RAG"],"model")]
    for x,title,sub,kind in top:d.node(x,171,205,127,title,sub,kind)
    bottom=[(765,"Cloud LLM",["Tailored response"],"model"),
            (520,"Action module",["Warnings + guidance"],"output"),
            (275,"Human feedback",["Driver + expert", "review"],"control"),
            (30,"Knowledge base",["Curated RAG context"],"data")]
    for x,title,sub,kind in bottom:d.node(x,371,205,127,title,sub,kind)
    for a,b in [(235,275),(480,520),(725,765)]:d.edge([(a,234),(b,234)])
    d.edge([(867,298),(867,371)])
    for a,b in [(765,725),(520,480),(275,235)]:d.edge([(a,434),(b,434)])
    d.edge([(30,434),(15,434),(15,126),(867,126),(867,171)])
    d.text(632,119,"Retrieved context",18,"#74889d",anchor="middle")
    d.note("Responses return via available terrestrial/NTN links; reviewed feedback curates future retrieval context.")
    return d


def security():
    d = Diagram("split-learning-security", "Secure split-learning admission", "Two-stage screening | AI risk ranking + Hashcash verification",
                "A client's request packet is scored by an AI risk ranker. Low-risk clients receive a risk-adapted Hashcash challenge. "
                "A correct and timely client solution admits the client to split learning. High-risk requests and invalid or late solutions enter a blocklist. "
                "The offline ranker pipeline uses CIC-IDS2017, recursive feature elimination, and TVAE-based data augmentation.",
                "paper", ["Security and Efficiency Enhancement for Split Learning, Fig. 1-2 and Sec. III, PDF pp. 2-4"])
    d.text(500,132,"Offline ranker training: CIC-IDS2017 > RFE + TVAE > risk scoring",19,"#71869c",anchor="middle")
    d.node(30,183,205,132,"Client request",["Network packet"],"data")
    d.node(275,183,205,132,"AI risk ranking",["P(malicious)"],"model")
    d.node(520,183,205,132,"Hashcash gate",["Risk-adapted puzzle", "Verify client solution"],"control")
    d.node(765,183,205,132,"Admit client",["Split-learning task"],"output")
    d.node(520,392,205,110,"Blocklist",["Deny for a set period"],"control")
    d.edge([(235,249),(275,249)])
    d.edge([(480,249),(520,249)],label="low risk",at=(500,170))
    d.edge([(725,249),(765,249)],label="valid + timely",at=(746,170))
    d.edge([(377,315),(377,447),(520,447)],label="high risk",at=(414,423))
    d.edge([(622,315),(622,392)],label="invalid / late",at=(705,359))
    d.note("Risk thresholds, puzzle difficulty, response time, and blocklist duration are configurable policy parameters.")
    return d


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = [make().save() for make in
                [healthcare, edge_llm, allocation, formula, commerce, crs, vehicular, security]]
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Built {len(manifest)} system models in {OUT}")
