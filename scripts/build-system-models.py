"""Build original system-architecture SVGs, with deployment/module boundaries.

The diagrams identify hosts, application/model components, storage, and data,
response, and control connections. Source metadata lives in the editable catalog.
Python standard library only; rendered assets have no website dependencies.
"""
from pathlib import Path
from html import escape
import json
import math
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/models'
CATALOG = {m['slug']: m for m in json.loads((ROOT/'scripts/system-model-catalog.json').read_text(encoding='utf-8'))}
W, H = 1200, 760
COLORS = {
    'data': ('#edf4fc', '#bed1e5', '#355c7c'),
    'model': ('#f0f1fb', '#c8cde6', '#4b5e84'),
    'control': ('#fff5e6', '#e4cda9', '#8a6637'),
    'output': ('#eaf6f1', '#afd3c4', '#39725f'),
}


def lines(text, width, size):
    if isinstance(text, list):
        return text
    return textwrap.wrap(text, max(7, int(width/(size*.55))), break_long_words=False, break_on_hyphens=False)


class Architecture:
    def __init__(self, slug, subtitle):
        self.meta = dict(CATALOG[slug]); self.slug = slug; self.subtitle = subtitle
        self.back, self.edges, self.front = [], [], []
        self.checks = []

    def text(self, x, y, text, size=21, color='#4f657c', weight=400, anchor='start', layer='front'):
        getattr(self,layer).append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
                                  f'font-size="{size}" font-weight="{weight}" fill="{color}" '
                                  f'text-anchor="{anchor}">{escape(text)}</text>')

    def zone(self, x, y, w, h, title, sub='', icon=None):
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="17" '
                         'fill="#fff" stroke="#c9d6e4" stroke-width="2"/>')
        self.back.append(f'<path d="M {x+1} {y+66} H {x+w-1}" stroke="#e2e8ef" stroke-width="1.5"/>')
        self.text(x+20,y+28,title,20,'#35516b',600,layer='back')
        if sub:self.text(x+20,y+51,sub,16,'#8190a2',layer='back')
        if icon:self.icon(icon,x+w-59,y+14,38,layer='back')

    def unit(self, x, y, w, h, title, sub='', kind='model'):
        assert x>=20 and y>=118 and x+w<=1180 and y+h<=663,(self.slug,title,x,y,w,h)
        fill,stroke,ink=COLORS[kind]
        self.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="11" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="1.7"/>')
        title_lines=lines(title,w-24,22);sub_lines=lines(sub,w-24,17) if sub else []
        total=26*len(title_lines)+21*len(sub_lines)+(6 if sub_lines else 0)
        assert total<=h-12,(self.slug,title,total,h)
        baseline=y+(h-total)/2+21
        for line in title_lines:
            self.text(x+w/2,round(baseline,1),line,22,ink,600,'middle')
            self.checks.append([line,w-20,22,600]);baseline+=26
        if sub_lines:baseline+=4
        for line in sub_lines:
            self.text(x+w/2,round(baseline,1),line,17,'#6a7d90',400,'middle')
            self.checks.append([line,w-20,17,400]);baseline+=21

    def database(self,x,y,w,h,title,sub=''):
        self.front.append(f'<path d="M {x} {y+16} V {y+h-16} C {x} {y+h+6} {x+w} {y+h+6} {x+w} {y+h-16} '
                          f'V {y+16} Z" fill="#edf4fc" stroke="#bcd0e4" stroke-width="1.8"/>')
        self.front.append(f'<ellipse cx="{x+w/2}" cy="{y+16}" rx="{w/2}" ry="16" '
                          'fill="#f7faff" stroke="#bcd0e4" stroke-width="1.8"/>')
        title_lines=lines(title,w-20,21);sub_lines=lines(sub,w-20,16) if sub else []
        baseline=y+43
        for t in title_lines:self.text(x+w/2,baseline,t,21,'#3b6284',600,'middle');baseline+=25
        for t in sub_lines:self.text(x+w/2,baseline+3,t,16,'#6a7f94',400,'middle');baseline+=20

    def icon(self,kind,x,y,size=44,layer='front'):
        dest=getattr(self,layer);stroke='#7b93aa';s=size
        if kind=='server':
            for dy in [0,.32,.64]:
                dest.append(f'<rect x="{x}" y="{y+s*dy}" width="{s}" height="{s*.25}" rx="3" fill="#edf3fa" stroke="{stroke}" stroke-width="1.4"/>')
                dest.append(f'<circle cx="{x+s*.17}" cy="{y+s*(dy+.125)}" r="{s*.035}" fill="{stroke}"/>')
                dest.append(f'<path d="M {x+s*.38} {y+s*(dy+.125)} H {x+s*.85}" stroke="{stroke}"/>')
        elif kind=='device':
            dest.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s*.7}" rx="4" fill="#edf3fa" stroke="{stroke}" stroke-width="1.6"/>')
            dest.append(f'<path d="M {x+s*.5} {y+s*.7} V {y+s*.92} M {x+s*.22} {y+s*.92} H {x+s*.78}" stroke="{stroke}" stroke-width="1.6"/>')
        elif kind=='network':
            for r in [.2,.38,.56]:
                dest.append(f'<path d="M {x+s*(.5-r)} {y+s*.6} Q {x+s*.5} {y+s*(.6-r)} {x+s*(.5+r)} {y+s*.6}" fill="none" stroke="{stroke}" stroke-width="2.2"/>')
            dest.append(f'<circle cx="{x+s*.5}" cy="{y+s*.72}" r="{s*.055}" fill="{stroke}"/>')
        elif kind=='satellite':
            dest.append(f'<rect x="{x+s*.37}" y="{y+s*.25}" width="{s*.26}" height="{s*.42}" rx="5" fill="#dae7f4" stroke="{stroke}" stroke-width="2"/>')
            for dx in [.02,.7]:
                dest.append(f'<rect x="{x+s*dx}" y="{y+s*.31}" width="{s*.28}" height="{s*.3}" fill="#c3d6eb" stroke="{stroke}" stroke-width="1.8"/>')
            dest.append(f'<path d="M {x+s*.5} {y+s*.67} V {y+s*.86} M {x+s*.34} {y+s*.9} Q {x+s*.5} {y+s*.76} {x+s*.66} {y+s*.9}" fill="none" stroke="{stroke}" stroke-width="1.8"/>')

    def client(self,x,y,w,h,title,layers):
        self.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h-17}" rx="11" fill="#edf4fc" stroke="#b9cfe5" stroke-width="2"/>')
        self.text(x+w/2,y+29,title,21,'#3d6281',600,'middle')
        for i in range(3):
            self.front.append(f'<rect x="{x+37+i*42}" y="{y+46}" width="27" height="28" rx="4" fill="#c6d9ee" stroke="#a5bed7"/>')
        self.text(x+w/2,y+99,layers,17,'#607b96',anchor='middle')
        self.text(x+w/2,y+122,'Private local data',16,'#7b8fa3',anchor='middle')
        self.front.append(f'<path d="M {x+w*.43} {y+h-17} V {y+h-3} H {x+w*.25} H {x+w*.75}" fill="none" stroke="#a9bed2" stroke-width="2"/>')

    def branch(self,x,y,w,h,title,components):
        self.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#f0f1fb" stroke="#c7cde5" stroke-width="1.8"/>')
        self.text(x+15,y+29,title,20,'#4d5f83',600)
        for i,label in enumerate(components):
            cy=y+46+i*48
            self.front.append(f'<rect x="{x+14}" y="{cy}" width="{w-28}" height="39" rx="6" fill="white" stroke="#d4d9eb"/>')
            self.text(x+w/2,cy+25,label,17,'#5a6d89',anchor='middle')

    def edge(self,points,kind='data',label=None,at=None):
        color={'data':'#718eaa','control':'#b08b55','feedback':'#5d9b87'}[kind]
        if kind=='control':
            parts=[]
            for (x1,y1),(x2,y2) in zip(points,points[1:]):
                dist=math.hypot(x2-x1,y2-y1)
                if not dist:continue
                ux,uy=(x2-x1)/dist,(y2-y1)/dist
                for t in range(0,math.ceil(dist),13):
                    stop=min(t+7,dist);parts.append(f'M {x1+ux*t:.1f} {y1+uy*t:.1f} L {x1+ux*stop:.1f} {y1+uy*stop:.1f}')
            path=' '.join(parts)
        else:path='M '+' L '.join(f'{x} {y}' for x,y in points)
        self.edges.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linejoin="round"/>')
        (x1,y1),(x2,y2)=points[-2:];dist=math.hypot(x2-x1,y2-y1);ux,uy=(x2-x1)/dist,(y2-y1)/dist
        tx,ty=x2-ux*2,y2-uy*2;bx,by=tx-ux*9,ty-uy*9
        self.edges.append(f'<polygon points="{tx:.1f},{ty:.1f} {bx-uy*4.5:.1f},{by+ux*4.5:.1f} {bx+uy*4.5:.1f},{by-ux*4.5:.1f}" fill="{color}"/>')
        if label:
            assert at
            self.text(at[0],at[1],label,16,color,anchor='middle')

    def note(self,text):
        for i,t in enumerate(lines(text,1128,18)):
            self.text(36,683+i*21,t,18,'#7a8ca0')

    def save(self):
        self.text(34,46,self.meta['title'],30,'#29465f',600)
        self.text(35,80,self.subtitle,20,'#74899d')
        self.back.insert(0,'<path d="M 30 104 H 1170" stroke="#dce5ee" stroke-width="1.5"/>')
        for x,color,label,dash in [(36,'#718eaa','Data / model traffic',False),(420,'#b08b55','Policy / training signals',True),(820,'#5d9b87','Response / feedback',False)]:
            if dash:
                path=' '.join(f'M {x+i} 731 H {x+i+7}' for i in range(0,40,13))
            else:path=f'M {x} 731 H {x+43}'
            self.front.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.5"/>')
            self.text(x+54,737,label,17,'#7c8da0')
        svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">'
             f'<title id="title">{escape(self.meta["title"])} - system architecture</title><desc id="desc">{escape(self.meta["description"])}</desc>'
             '<rect x="1" y="1" width="1198" height="758" rx="20" fill="#f8fafc" stroke="#dfe7ef"/>'
             +''.join(self.back+self.edges+self.front)+'</svg>')
        (OUT/f'{self.slug}.svg').write_text(svg,encoding='utf-8')
        return {**self.meta,'width':W,'height':H,'representation':'system-architecture','text_checks':self.checks}


def healthcare():
    d=Architecture('healthcare-pipeline','System architecture | data sources, ML components, and secure deployment')
    d.zone(28,140,250,482,'Clinical evidence','Input boundary')
    d.database(50,240,206,112,'Clinical records','Multimodal data')
    d.unit(50,440,206,112,'Evidence quality',['Missing data','Class imbalance'],'data')
    d.zone(340,140,832,482,'Secure HPC environment','ML application boundary','server')
    d.unit(365,237,235,126,'Preprocessing',['Data preparation','Quality handling'],'model')
    d.unit(640,237,235,126,'Feature extraction',['Multimodal','representations'],'model')
    d.unit(915,237,232,126,'Risk prediction',['Clinical ML models'],'model')
    d.unit(390,459,300,112,'Model evaluation',['Performance assessment'],'output')
    d.database(760,464,350,99,'Analysis outputs','Predictions and evaluation')
    d.edge([(256,296),(365,296)])
    d.edge([(256,496),(312,496),(312,333),(365,333)],'control')
    d.edge([(600,300),(640,300)])
    d.edge([(875,300),(915,300)])
    d.edge([(1031,363),(1031,407),(540,407),(540,459)])
    d.edge([(690,515),(760,515)])
    d.note('Project-level logical architecture; the HPC boundary identifies the supplied deployment environment.')
    return d


def edge_llm():
    d=Architecture('edge-llm','Conceptual system architecture | device, wireless network, and edge server')
    d.zone(28,145,330,470,'Device','Local inference boundary','device')
    d.unit(52,232,282,94,'Request context','Prompt and local inputs','data')
    d.unit(52,372,282,135,'LLM prefix',['Layers 1 .. s','Device-side execution'],'model')
    d.unit(52,543,282,58,'Response consumer',kind='output')
    d.zone(794,145,378,470,'Wireless edge server','Remote inference boundary','server')
    d.unit(818,232,330,135,'Remaining LLM',['Layers s+1 .. L','Edge-side execution'],'model')
    d.unit(818,430,330,116,'Inference runtime','Server compute resources','model')
    d.icon('network',520,205,104)
    d.text(572,335,'Wireless network',21,'#52728f',600,'middle')
    d.unit(420,450,300,141,'Value-aware coordinator',['Split points and','resource allocation'],'control')
    d.edge([(193,326),(193,372)])
    d.edge([(334,425),(393,425),(393,303),(478,303)])
    d.edge([(666,303),(818,303)])
    d.edge([(1148,299),(1186,299),(1186,642),(193,642),(193,601)],'feedback',label='Generated response',at=(895,634))
    d.edge([(983,430),(983,367)],'control')
    d.edge([(420,521),(378,521),(378,477),(334,477)],'control')
    d.edge([(720,521),(773,521),(773,488),(818,488)],'control')
    d.edge([(570,450),(570,355)],'control')
    d.note('Conceptual deployment architecture for the under-review manuscript; no specific model or latency result is assumed.')
    return d


def allocation():
    d=Architecture('federated-partitioning','System architecture | heterogeneous clients and a shared server compute pool')
    d.zone(28,140,1144,284,'Central federated-learning server','Shared model-compute boundary','server')
    d.unit(52,232,280,132,'JCRALP controller',['Layer split points','Server CPU allocation'],'control')
    d.unit(385,223,760,70,'Shared CPU pool',['Sum of client shares <= server budget'],'control')
    for x,name in [(385,'1'),(660,'2'),(935,'N')]:
        d.unit(x,315,210,90,'Server tail '+name,['Layers s'+name+'+1 .. L'],'model')
        d.edge([(x+105,293),(x+105,315)],'control')
    d.edge([(332,298),(357,298),(357,255),(385,255)],'control')
    d.unit(52,490,270,146,'Heterogeneous clients',['Local compute, energy,','and dataset volumes'],'data')
    for x,name in [(378,'1'),(653,'2'),(928,'N')]:
        cx=x+112
        d.client(x,480,224,165,'Client '+name,'Prefix layers 1 .. s'+name)
        d.edge([(cx-12,480),(cx-12,405)])
        d.edge([(cx+12,405),(cx+12,480)],'feedback')
    d.text(52,452,'Client activations to server',17,'#718eaa')
    d.text(52,476,'Server gradients to clients',17,'#5d9b87')
    d.note('JCRALP uses optimization for profiled systems or modified TD3 when system parameters are uncertain.')
    return d


def crs():
    d=Architecture('crs-triage','Model architecture | modality branches, evidential fusion, and a selective decision interface')
    d.zone(28,140,210,484,'Encounter inputs','Clinical evidence')
    d.unit(49,240,168,128,'Structured data',['Values and','missingness mask'],'data')
    d.unit(49,449,168,100,'Clinical text',['Triage text'],'data')
    d.zone(280,140,620,484,'CRS-Triage model','Jointly trained multimodal architecture')
    d.branch(304,235,250,152,'Structured branch',['Value / mask encoder','Structured evidence head'])
    d.branch(304,441,250,152,'Text branch',['Clinical text encoder','Text evidence head'])
    d.unit(610,229,266,78,'Fusion weights',['Reliability + agreement'],'control')
    d.unit(610,341,266,132,'Evidence fusion',['Reliability + uncertainty','Cross-modal consistency'],'model')
    d.unit(610,523,266,85,'Confidence head',['Selective objective'],'control')
    d.zone(940,140,232,484,'Decision interface','Probabilities and deferral')
    d.unit(964,240,184,103,'Class probabilities',['p'],'output')
    d.unit(964,411,184,120,'Selection gate',['s compared with tau'],'control')
    d.unit(964,550,184,60,['Predict / defer'],kind='output')
    d.edge([(217,304),(304,304)])
    d.edge([(217,499),(304,499)])
    d.edge([(554,311),(582,311),(582,384),(610,384)])
    d.edge([(554,517),(582,517),(582,432),(610,432)])
    d.edge([(743,307),(743,341)],'control')
    d.edge([(743,473),(743,523)])
    d.edge([(876,390),(920,390),(920,292),(964,292)])
    d.edge([(876,566),(920,566),(920,465),(964,465)],'control')
    d.edge([(1056,343),(1056,411)])
    d.edge([(1056,531),(1056,550)])
    d.note('Joint training: evidential learning + triage penalty + selective prediction + cross-modal disagreement.')
    return d


def formula():
    d=Architecture('formula-recognition','Conceptual architecture | visual recognition components and structured output')
    d.front.append('<path d="M 40 250 H 170 L 210 290 V 527 H 40 Z" fill="white" stroke="#bbcee2" stroke-width="2"/>')
    d.front.append('<path d="M 170 250 V 290 H 210" fill="none" stroke="#bbcee2" stroke-width="2"/>')
    for y in [315,344,458,487]:d.front.append(f'<path d="M 61 {y} H 184" stroke="#dce5ee" stroke-width="5"/>')
    d.front.append('<rect x="61" y="371" width="123" height="60" rx="5" fill="#edf4fc" stroke="#99b8d6" stroke-dasharray="5 4"/>')
    d.text(122,410,'a / b',27,'#547592',anchor='middle')
    d.text(125,563,'Document image',20,'#526f8c',600,'middle')
    d.zone(270,140,640,484,'Document recognition system','Logical application boundary')
    d.unit(296,251,250,126,'Formula localizer',['Detection + extraction'],'model')
    d.branch(580,234,305,152,'Recognition components',['Symbol recognition','2D structure parsing'])
    d.unit(296,466,589,107,'LaTeX serializer',['Build a structured, editable expression'],'model')
    d.unit(952,302,220,170,'Editable LaTeX',['Output format example:','\\frac{a}{b}'],'output')
    d.edge([(210,401),(244,401),(244,314),(296,314)])
    d.edge([(546,314),(580,314)])
    d.edge([(732,386),(732,466)])
    d.edge([(885,519),(929,519),(929,387),(952,387)])
    d.note('Conceptual module architecture; the fraction illustrates output syntax and is not an accuracy claim.')
    return d


def commerce():
    d=Architecture('commerce-automation','Conceptual application architecture | users, business modules, and SQL persistence')
    d.icon('device',80,274,110)
    d.text(137,437,'Internal users',22,'#4f6d88',600,'middle')
    d.zone(285,140,615,484,'Java / Spring Boot application','Application boundary')
    d.unit(315,230,555,83,'Application interface',['Internal procurement requests'],'data')
    for x,title in [(315,'Quotations'),(510,'Invoicing'),(705,'Suppliers')]:
        d.unit(x,368,165,117,title,['Business module'],'model')
        d.edge([(592,313),(592,340),(x+82,340),(x+82,368)])
    d.unit(315,541,555,65,'SQL persistence access',kind='model')
    for x in [397,592,787]:d.edge([(x,485),(x,514),(592,514),(592,541)])
    d.database(950,299,222,182,'SQL data store',['Quotation, invoice,','and supplier records'])
    d.edge([(190,329),(247,329),(247,271),(315,271)])
    d.edge([(315,290),(265,290),(265,385),(190,385)],'feedback')
    d.edge([(870,563),(924,563),(924,363),(950,363)])
    d.edge([(950,415),(936,415),(936,590),(870,590)],'feedback')
    d.note('Conceptual application architecture from the project description; no specific UI framework or database engine is assumed.')
    return d


def vehicular():
    d=Architecture('vehicular-llm','System architecture | vehicle-side intelligence, communication network, and cloud services')
    d.zone(28,140,360,490,'Vehicle-side system','Jetson Nano prototype','device')
    d.unit(52,236,146,100,'Sensor inputs',kind='data')
    d.unit(218,236,146,100,'Driver profile',kind='data')
    d.unit(52,378,312,100,'On-board query LLM',['Gemma3 1B (prototype)'],'model')
    d.unit(52,519,312,95,'Action + feedback',['Warnings and driver feedback'],'output')
    d.zone(782,140,390,490,'Cloud-side services','Server: 3 RTX 3090 GPUs','server')
    d.unit(805,236,342,113,'Query augmentation + RAG',['Historical queries and context'],'model')
    d.unit(805,404,342,90,'Response LLM',['LLaMA 30B (prototype)'],'model')
    d.database(805,541,200,76,'Knowledge base')
    d.unit(1022,531,125,89,'Review',['Expert','curation'],'control')
    d.icon('satellite',524,228,140)
    d.text(595,406,'Communication',23,'#52728e',600,'middle')
    d.text(595,435,'Terrestrial / NTN',18,'#7890a7',anchor='middle')
    d.edge([(125,336),(125,378)])
    d.edge([(291,336),(291,378)])
    d.edge([(364,414),(437,414),(437,340),(492,340)])
    d.edge([(697,340),(751,340),(751,280),(805,280)])
    d.edge([(976,349),(976,404)])
    d.edge([(805,462),(697,462)],'feedback')
    d.edge([(492,462),(432,462),(432,555),(364,555)],'feedback')
    d.edge([(364,588),(412,588),(412,651),(1084,651),(1084,620)],'feedback')
    d.edge([(976,494),(976,513),(1084,513),(1084,531)],'feedback')
    d.edge([(1022,575),(1005,575)],'feedback')
    d.edge([(905,541),(905,516),(768,516),(768,323),(805,323)])
    d.note('NTN is part of the proposed architecture; the reported hardware prototype used a local-network connection.')
    return d


def security():
    d=Architecture('split-learning-security','System architecture | untrusted client, admission gateway, and protected learning service')
    d.zone(28,145,260,480,'Client side','Untrusted requests','device')
    d.unit(52,254,212,118,'Client agent',['Packet sender','Hashcash solver'],'data')
    d.text(157,504,'Request + proof',20,'#607b96',600,'middle')
    d.zone(355,145,525,480,'Server admission gateway','Security boundary','server')
    d.unit(380,240,220,110,'AI risk ranker',['Maliciousness score'],'model')
    d.unit(635,240,220,110,'Hashcash service',['Challenge + verification'],'control')
    d.unit(380,436,220,106,'Policy settings',['Risk threshold','Timeout / difficulty'],'control')
    d.database(635,443,220,102,'Blocklist','Temporary denial')
    d.zone(945,145,225,300,'Protected server','Split-learning backend')
    d.icon('server',1014,258,87)
    d.text(1057,399,'Training service',20,'#4e6b88',600,'middle')
    d.unit(945,494,225,132,'Offline risk model',['CIC-IDS2017','RFE + TVAE training'],'model')
    d.edge([(264,282),(324,282),(324,218),(490,218),(490,240)])
    d.edge([(600,295),(635,295)])
    d.edge([(855,281),(945,281)],label='Admit',at=(899,265))
    d.edge([(670,350),(670,390),(310,390),(310,316),(264,316)],'feedback')
    d.edge([(264,352),(330,352),(330,411),(805,411),(805,350)])
    d.edge([(380,315),(348,315),(348,579),(745,579),(745,545)],label='High risk',at=(440,570))
    d.edge([(855,330),(906,330),(906,493),(855,493)])
    d.text(894,432,'Invalid / late',16,'#718eaa',anchor='end')
    d.edge([(490,436),(490,350)],'control')
    d.edge([(600,489),(615,489),(615,369),(701,369),(701,350)],'control')
    d.edge([(945,557),(922,557),(922,220),(620,220),(620,262),(600,262)],'control')
    d.note('The gateway uses packet-risk ranking and proof-of-work verification before admitting clients to the learning backend.')
    return d


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=[fn().save() for fn in [healthcare,edge_llm,allocation,formula,commerce,crs,vehicular,security]]
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(f'Built {len(manifest)} system architectures in {OUT}')
