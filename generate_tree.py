#!/usr/bin/env python3
"""
generate_tree.py
================
Generates index.html for the Perez · Zitt Family Tree.

Usage:
    python3 generate_tree.py            # writes index.html to current directory
    python3 generate_tree.py --preview  # opens the result in a browser

All family data lives in the DATA section below.
Edit data here → run script → commit index.html → GitHub Pages auto-updates.
"""

import sys
import textwrap
from pathlib import Path

# ══════════════════════════════════════════════════════════════════
#  DATA  —  edit this section to update the tree
# ══════════════════════════════════════════════════════════════════

HEADER = {
    "title":    "Perez · Zitt Family Tree",
    "subtitle": "Juan Miguel Perez &amp; Melissa Perez (née Zitt) &nbsp;·&nbsp; Updated March 2026",
}

def person(id, name, maiden=None, dob=None, note=None, tag=None, css=None, side=None):
    return dict(id=id, name=name, maiden=maiden, dob=dob,
                note=note, tag=tag, css=css or [], side=side)

GRANDPARENTS = [
    ("perez", [
        person("gp-gonzalo", "Gonzalo Perez", dob="b. Unknown", tag="Grandfather"),
        person("gp-osiris",  "Osiris Perez",  maiden="née Ramos", dob="b. Unknown", tag="Grandmother"),
    ]),
    ("perez", [
        person("gp-evaristo", "Evaristo Santana", dob="b. Unknown", tag="Grandfather"),
        person("gp-zolia",    "Zolia Santana",    maiden="née Dalda", dob="b. Unknown", tag="Grandmother"),
    ]),
    ("zitt", [
        person("zp-gf", "Paternal Grandfather", maiden="Zitt family", dob="To be researched",
               tag="Grandfather", css=["unknown"]),
        person("zp-gm", "Paternal Grandmother", maiden="Zitt family", dob="To be researched",
               tag="Grandmother", css=["unknown"]),
    ]),
    ("zitt", [
        person("coppola-gf", "Louis Joseph Coppola", dob="b. Unknown", tag="Grandfather", css=["zitt"]),
        person("coppola-gm", "Anne Coppola", maiden="née Neri", dob="b. Unknown",
               tag="Grandmother", css=["zitt"]),
    ]),
]

PARENTS = [
    ("perez", [
        person("ana-osiris",  "Ana Osiris Martinez", maiden="née Perez", dob="b. Unknown",
               tag="Aunt (Paternal)", css=["cousin"]),
        person("antonio-sr",  "Antonio Martinez",   dob="b. Unknown", tag="Uncle", css=["cousin"]),
    ]),
    ("perez", [
        person("father", "Juan Gonzalo Perez", dob="b. June 11, 1955", tag="Father"),
        person("mother", "Zaida Perez", maiden="née Santana", dob="b. Sep 13, 1957", tag="Mother"),
    ]),
    ("perez_single", person("olga", "Olga", dob="b. Unknown", tag="Stepmother", css=["unknown"])),
    ("perez_single", person("dayanna-father", "Unknown Father", dob="b. Unknown",
                            tag="Dayanna's Father", css=["unknown"])),
    ("zitt", [
        person("dennis-zitt", "Dennis Herbert Zitt", dob="b. Apr 27, 1949",
               tag="Father-in-law", css=["zitt"]),
        person("anna-zitt",   "Anna Louise Zitt", maiden="née Coppola", dob="b. Mar 25, 1952",
               tag="Mother-in-law", css=["zitt"]),
    ]),
]

GEN3 = [
    ("perez_single", person("antonio-jr", "Antonio Martinez", dob="b. Unknown",
                            tag="Cousin", css=["cousin"])),
    ("perez", [
        person("ana-martinez",   "Ana Martinez",   maiden="now Ramirez", dob="b. Unknown",
               tag="Cousin", css=["cousin"]),
        person("daniel-ramirez", "Daniel Ramirez", dob="b. Unknown",
               tag="Cousin-in-law", css=["cousin"]),
    ]),
    ("perez", [
        person("gonzalo",      "Gonzalo E. Perez",  dob="b. July 27, 1976", tag="Brother"),
        person("maria-alfaro", "Maria Perez", maiden="née Alfaro", tag="Sister-in-law", css=["in-law"]),
    ]),
    (None, [
        person("juan",    "Juan Miguel Perez", dob="b. Oct 28, 1980", tag="You",    css=["you"]),
        person("melissa", "Melissa Perez", maiden="née Zitt", dob="b. Mar 15, 1981",
               tag="Spouse", css=["spouse"]),
    ]),
    ("perez", [
        person("daniel",   "Daniel Orlando Perez", dob="b. June 23, 1982", tag="Brother"),
        person("jennifer", "Jennifer Perez", maiden="née Safanova",
               tag="Sister-in-law", css=["in-law"]),
    ]),
    ("perez_single", person("joanna",  "Joanna Marie Perez", dob="b. 2005", tag="Half-Sister",  css=["half"])),
    ("perez_single", person("dayanna", "Dayanna", maiden="Last name TBD",
                            note="Olga's daughter (diff. father)",
                            tag="Joanna's Half-Sister", css=["half"])),
    ("zitt", [
        person("deanna",       "Deanna Marie Lebet", maiden="née Zitt", dob="b. Aug 13, 1969",
               tag="Sister-in-law", css=["zitt-sib"]),
        person("john-lebet-sr","John Lebet", tag="Brother-in-law", css=["in-law"]),
    ]),
    ("zitt", [
        person("patricia",       "Patricia Ann Welton", maiden="née Zitt", dob="b. June 12, 1971",
               tag="Sister-in-law", css=["zitt-sib"]),
        person("michael-welton", "Michael Welton", tag="Brother-in-law", css=["in-law"]),
    ]),
    ("zitt_single", person("dennis-wayne", "Dennis Wayne Zitt", dob="b. June 14, 1974",
                           note="Divorced · No children",
                           tag="Brother-in-law", css=["zitt-sib"])),
]

KIDS = [
    ("perez_single", person("melenia",   "Melenia Ramirez",    dob="b. Unknown", tag="2nd Cousin", css=["cousin"])),
    ("perez_single", person("alejandro", "Alejandro Ramirez",  dob="b. Unknown", tag="2nd Cousin", css=["cousin"])),
    ("perez_single", person("mya",       "Mya Ramirez",        dob="b. Unknown", tag="2nd Cousin", css=["cousin"])),
    ("perez_single", person("alexandria","Alexandria Ramirez",  dob="b. Unknown", tag="2nd Cousin", css=["cousin"])),
    ("perez_single", person("jamila",    "Jamila Ramirez", dob="b. Unknown",
                            note="Mother unknown", tag="2nd Cousin", css=["cousin"])),
    (None, person("julian", "Julian Lucas Perez",  dob="b. Feb 4, 2011",  tag="Son",      css=["child-m"])),
    (None, person("alexa",  "Alexa Santana Perez", dob="b. Feb 4, 2015",  tag="Daughter", css=["child-f"])),
    (None, person("sophia", "Sophia Quinn Perez",  dob="b. Oct 4, 2022",  tag="Daughter", css=["child-f"])),
    ("perez_single", person("sena", "Sena Sakura Perez", dob="b. April 2014",
                            tag="Niece", css=["child-f"])),
    ("zitt_single",  person("john-lebet-jr", "John Lebet",    dob="b. Unknown", tag="Nephew",  css=["niece-m"])),
    ("zitt_single",  person("kevin-lebet",   "Kevin Lebet",   dob="b. Unknown", tag="Nephew",  css=["niece-m"])),
    ("zitt_single",  person("matthew-lebet", "Matthew Lebet", dob="b. Unknown", tag="Nephew",  css=["niece-m"])),
    ("zitt_single",  person("kaitlyn",       "Kaitlyn", maiden="Different father",
                            tag="Niece",  css=["niece-f"])),
    ("zitt_single",  person("stephanie-welton", "Stephanie Welton", dob="b. Unknown", tag="Niece",   css=["niece-f"])),
    ("zitt_single",  person("brian-welton",     "Brian Welton",     dob="b. Unknown", tag="Nephew",  css=["niece-m"])),
]CSS = """
    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Georgia', serif;
      background: linear-gradient(160deg, #fdf6ec 0%, #f0e6d2 100%);
      min-height: 100vh;
      padding: 30px 0 60px;
    }

    header { text-align: center; margin-bottom: 16px; padding: 0 20px; }
    header h1 { font-size: 2em; color: #2c1a0e; letter-spacing: 3px; text-transform: uppercase; }
    header p  { color: #9b7340; font-style: italic; margin-top: 4px; font-size: 0.9em; }

    .toggle-bar {
      display: flex; justify-content: center; gap: 10px;
      margin-bottom: 16px; flex-wrap: wrap;
    }
    .toggle-bar button {
      font-family: 'Georgia', serif;
      font-size: 0.82em; letter-spacing: 0.5px;
      padding: 7px 20px; border-radius: 25px; cursor: pointer;
      border: 2px solid #d4b896; background: #fff; color: #7d4e1e;
      transition: all .18s;
    }
    .toggle-bar button:hover { background: #f8ece0; }
    .toggle-bar button.active { background: #9b7340; color: #fff; border-color: #9b7340; }
    .toggle-bar button.active.zitt-btn { background: #2471a3; border-color: #2471a3; }

    .tree-mode-perez .zitt-side { display: none !important; }
    .tree-mode-zitt  .perez-side { display: none !important; }

    #tree-scroll { overflow-x: auto; padding: 0 20px 20px; }

    #tree {
      position: relative;
      min-width: 3800px;
      padding: 0 10px 20px;
    }

    #svg-lines {
      position: absolute; top: 0; left: 0;
      width: 100%; height: 100%;
      pointer-events: none; z-index: 0; overflow: visible;
    }

    .gen-row {
      display: flex; justify-content: center;
      align-items: flex-start; gap: 9px;
      margin-bottom: 62px; position: relative;
      z-index: 1; flex-wrap: nowrap;
    }

    .gen-label {
      text-align: center; font-size: 0.64em;
      letter-spacing: 2px; text-transform: uppercase;
      color: #b89060; margin-bottom: 7px;
    }

    .fam-gap { flex: 0 0 60px; align-self: center; height: 2px;
               background: linear-gradient(90deg, transparent, #d4b896 50%, transparent); }
    .v-sep   { flex: 0 0 1px; height: 50px; border-left: 2px dashed #ccc;
               align-self: center; margin: 0 5px; }

    .couple { display: flex; align-items: center; gap: 3px; flex-shrink: 0; }
    .heart  { font-size: 1.1em; color: #c0392b; flex-shrink: 0; }
    .heart.div { color: #bbb; font-style: normal; font-size: 0.9em; }

    .card {
      background: #fff; border: 2px solid #d4b896;
      border-radius: 10px; padding: 9px 10px; width: 132px;
      text-align: center; box-shadow: 0 2px 7px rgba(0,0,0,0.08);
      transition: transform .18s, box-shadow .18s; flex-shrink: 0;
    }
    .card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.13); }

    .card.you      { border-color: #c0392b; background: #fff5f5; border-width: 3px; }
    .card.spouse   { border-color: #7d3c98; border-style: dashed; }
    .card.half     { border-color: #1e8449; border-style: dashed; }
    .card.child-m  { border-color: #2980b9; }
    .card.child-f  { border-color: #c0397b; }
    .card.unknown  { border-color: #b0b0b0; border-style: dotted; background: #f8f8f8; }
    .card.zitt     { border-color: #2471a3; background: #f0f6fc; }
    .card.zitt-sib { border-color: #2471a3; }
    .card.cousin   { border-color: #6c3483; background: #fdf2ff; }
    .card.tbd      { border-color: #aaa; border-style: dashed; background: #fafafa; }
    .card.divorced { border-color: #bbb; background: #f7f7f7; opacity: 0.85; }
    .card.in-law   { border-color: #888; }
    .card.niece-m  { border-color: #1a7abf; }
    .card.niece-f  { border-color: #b0306a; }

    .card .name   { font-size: 0.77em; font-weight: bold; color: #2c1a0e; line-height: 1.3; }
    .card .maiden { font-size: 0.63em; color: #9b7340; font-style: italic; margin-top: 2px; }
    .card .dob    { font-size: 0.64em; color: #777; margin-top: 4px; }
    .card .note   { font-size: 0.6em; color: #999; font-style: italic; margin-top: 3px; }
    .card .tag {
      display: inline-block; font-size: 0.58em; color: #fff;
      background: #9b7340; border-radius: 20px;
      padding: 2px 7px; margin-top: 5px; letter-spacing: 0.3px;
    }
    .card.you    .tag  { background: #c0392b; }
    .card.spouse .tag  { background: #7d3c98; }
    .card.half   .tag  { background: #1e8449; }
    .card.unknown .tag { background: #999; }
    .card.child-m .tag { background: #2980b9; }
    .card.child-f .tag { background: #c0397b; }
    .card.zitt .tag, .card.zitt-sib .tag { background: #2471a3; }
    .card.cousin  .tag { background: #6c3483; }
    .card.tbd     .tag { background: #aaa; }
    .card.divorced .tag { background: #888; }
    .card.in-law  .tag { background: #666; }
    .card.niece-m .tag { background: #1a7abf; }
    .card.niece-f .tag { background: #b0306a; }

    .banner-row { display: flex; justify-content: space-between; align-items: center;
                  margin-bottom: 5px; padding: 0 30px; }
    .side-banner { font-size: 0.7em; font-weight: bold; letter-spacing: 1px;
                   padding: 4px 12px; border-radius: 20px; display: inline-block; }.side-banner.perez { background: #f8ece0; color: #7d4e1e; border: 1px solid #d4b896; }
    .side-banner.zitt  { background: #e8f0fb; color: #1a4a7a; border: 1px solid #90b8d8; }

    #legend { display: flex; justify-content: center; gap: 14px; flex-wrap: wrap;
              margin-top: 10px; padding: 0 20px; }
    .legend-item { display: flex; align-items: center; gap: 6px; font-size: 0.72em; color: #555; }
    .legend-box  { width: 18px; height: 11px; border-radius: 3px; border: 2px solid; }
"""

JS = """
// ── Toggle ──
function setMode(mode) {
  const tree = document.getElementById('tree');
  tree.classList.remove('tree-mode-perez','tree-mode-zitt');
  if (mode === 'perez') tree.classList.add('tree-mode-perez');
  if (mode === 'zitt')  tree.classList.add('tree-mode-zitt');
  ['all','perez','zitt'].forEach(m => {
    const b = document.getElementById('btn-'+m);
    b.classList.toggle('active', m === mode);
  });
  setTimeout(draw, 120);
}

function rel(id) {
  const el = document.getElementById(id);
  if (!el || el.offsetParent === null) return null;
  const b = el.getBoundingClientRect();
  const t = document.getElementById('tree').getBoundingClientRect();
  return {
    cx: b.left-t.left+b.width/2, cy: b.top-t.top+b.height/2,
    top: b.top-t.top, bottom: b.bottom-t.top,
    left: b.left-t.left, right: b.right-t.left,
  };
}

function ln(svg,x1,y1,x2,y2,col,dash) {
  const l=document.createElementNS('http://www.w3.org/2000/svg','line');
  l.setAttribute('x1',x1); l.setAttribute('y1',y1);
  l.setAttribute('x2',x2); l.setAttribute('y2',y2);
  l.setAttribute('stroke',col||'#c4a06a'); l.setAttribute('stroke-width','2');
  if(dash) l.setAttribute('stroke-dasharray','6 4');
  svg.appendChild(l);
}

function tee(svg,px,py,kids,col,dash) {
  kids=(kids||[]).filter(Boolean);
  if(!kids.length) return;
  const xs=kids.map(k=>k.cx);
  const barY=py+(kids[0].top-py)*0.5;
  ln(svg,px,py,px,barY,col,dash);
  if(kids.length>1) ln(svg,Math.min(...xs),barY,Math.max(...xs),barY,col,dash);
  kids.forEach(k=>ln(svg,k.cx,barY,k.cx,k.top,col,dash));
}

function draw() {
  const svg=document.getElementById('svg-lines');
  const tree=document.getElementById('tree');
  svg.innerHTML='';
  svg.setAttribute('width',tree.offsetWidth);
  svg.setAttribute('height',tree.offsetHeight);

  const C='#c4a06a', BL='#2471a3', GR='#1e8449', OR='#d35400';
  const PU='#6c3483', KB='#2980b9';

  const gpG=rel('gp-gonzalo'),gpO=rel('gp-osiris'),father=rel('father'),anaO=rel('ana-osiris');
  if(gpG&&gpO&&father&&anaO) tee(svg,(gpG.cx+gpO.cx)/2,Math.max(gpG.bottom,gpO.bottom),[anaO,father],C);

  const gpE=rel('gp-evaristo'),gpZ=rel('gp-zolia'),mother=rel('mother');
  if(gpE&&gpZ&&mother) tee(svg,(gpE.cx+gpZ.cx)/2,Math.max(gpE.bottom,gpZ.bottom),[mother],C);

  const zpgf=rel('zp-gf'),zpgm=rel('zp-gm'),dZitt=rel('dennis-zitt');
  if(zpgf&&zpgm&&dZitt) tee(svg,(zpgf.cx+zpgm.cx)/2,Math.max(zpgf.bottom,zpgm.bottom),[dZitt],BL,true);

  const cgf=rel('coppola-gf'),cgm=rel('coppola-gm'),aZitt=rel('anna-zitt');
  if(cgf&&cgm&&aZitt) tee(svg,(cgf.cx+cgm.cx)/2,Math.max(cgf.bottom,cgm.bottom),[aZitt],BL);

  const gonzalo=rel('gonzalo'),juan=rel('juan'),daniel=rel('daniel');
  if(father&&mother&&gonzalo&&juan&&daniel)
    tee(svg,(father.right+mother.left)/2,Math.max(father.bottom,mother.bottom),[gonzalo,juan,daniel],C);
  else if(father&&mother&&juan)
    tee(svg,(father.right+mother.left)/2,Math.max(father.bottom,mother.bottom),[juan],C);

  const olga=rel('olga'),joanna=rel('joanna');
  if(father&&olga&&joanna){
    const ux=(father.cx+olga.cx)/2,fBy=father.bottom;
    ln(svg,father.cx,fBy,father.cx,fBy+14,GR,true);
    ln(svg,father.cx,fBy+14,ux,fBy+14,GR,true);
    ln(svg,ux,fBy+14,ux,olga.bottom,GR,true);
    tee(svg,ux,olga.bottom,[joanna],GR,true);
  }

  const dayF=rel('dayanna-father'),dayanna=rel('dayanna');
  if(olga&&dayF&&dayanna){
    const ux=(olga.cx+dayF.cx)/2,oBy=olga.bottom;
    ln(svg,olga.cx,oBy,olga.cx,oBy+14,OR,true);
    ln(svg,olga.cx,oBy+14,ux,oBy+14,OR,true);
    ln(svg,ux,oBy+14,ux,Math.max(olga.bottom,dayF.bottom),OR,true);
    tee(svg,ux,Math.max(olga.bottom,dayF.bottom),[dayanna],OR,true);
  }

  const antJr=rel('antonio-jr'),anaMtz=rel('ana-martinez'),antSr=rel('antonio-sr');
  if(anaO&&antSr&&antJr&&anaMtz)
    tee(svg,(anaO.right+antSr.left)/2,Math.max(anaO.bottom,antSr.bottom),[antJr,anaMtz],PU);

  const deanna=rel('deanna'),patricia=rel('patricia'),dWayne=rel('dennis-wayne'),melissa=rel('melissa');
  if(dZitt&&aZitt&&melissa){
    const kids=[deanna,patricia,dWayne,melissa].filter(Boolean); tee(svg,(dZitt.right+aZitt.left)/2,Math.max(dZitt.bottom,aZitt.bottom),kids,BL);
  }  const dRam=rel('daniel-ramirez'),anaMart=rel('ana-martinez');
  const mel=rel('melenia'),ale=rel('alejandro'),mya2=rel('mya'),alex=rel('alexandria');
  if(anaMart&&dRam&&mel) tee(svg,(anaMart.right+dRam.left)/2,Math.max(anaMart.bottom,dRam.bottom),[mel,ale,mya2,alex].filter(Boolean),PU);

  const jamila=rel('jamila');
  if(dRam&&jamila){
    const midY=dRam.bottom+(jamila.top-dRam.bottom)*0.5;
    ln(svg,dRam.cx,dRam.bottom,dRam.cx,midY,PU,true);
    ln(svg,dRam.cx,midY,jamila.cx,midY,PU,true);
    ln(svg,jamila.cx,midY,jamila.cx,jamila.top,PU,true);
  }

  const danP=rel('daniel'),jennifer=rel('jennifer'),sena=rel('sena');
  if(danP&&jennifer&&sena) tee(svg,(danP.right+jennifer.left)/2,Math.max(danP.bottom,jennifer.bottom),[sena],C);

  const juanR=rel('juan'),melissaR=rel('melissa'),jul=rel('julian'),alx=rel('alexa'),soph=rel('sophia');
  if(juanR&&melissaR&&jul)
    tee(svg,(juanR.right+melissaR.left)/2,Math.max(juanR.bottom,melissaR.bottom),[jul,alx,soph].filter(Boolean),KB);

  const jLSr=rel('john-lebet-sr'),jJr=rel('john-lebet-jr'),kev=rel('kevin-lebet'),matt=rel('matthew-lebet');
  if(deanna&&jLSr&&jJr) tee(svg,(deanna.right+jLSr.left)/2,Math.max(deanna.bottom,jLSr.bottom),[jJr,kev,matt].filter(Boolean),BL);

  const mWelton=rel('michael-welton'),steph=rel('stephanie-welton'),brian=rel('brian-welton');
  if(patricia&&mWelton&&steph) tee(svg,(patricia.right+mWelton.left)/2,Math.max(patricia.bottom,mWelton.bottom),[steph,brian].filter(Boolean),BL);

  const kaitlyn=rel('kaitlyn');
  if(patricia&&kaitlyn){
    const midY=patricia.bottom+(kaitlyn.top-patricia.bottom)*0.5;
    ln(svg,patricia.cx,patricia.bottom,patricia.cx,midY,BL,true);
    ln(svg,patricia.cx,midY,kaitlyn.cx,midY,BL,true);
    ln(svg,kaitlyn.cx,midY,kaitlyn.cx,kaitlyn.top,BL,true);
  }
}

window.addEventListener('load', draw);
window.addEventListener('resize', draw);
"""

LEGEND_ITEMS = [
    ("#c0392b", "",        "You"),
    ("#d4b896", "",        "Perez family"),
    ("#7d3c98", "dashed",  "Spouse"),
    ("#6c3483", "#fdf2ff", "Cousin branch"),
    ("#2471a3", "#f0f6fc", "Zitt family"),
    ("#1e8449", "dashed",  "Half-sibling"),
    ("#2980b9", "",        "Son / Nephew"),
    ("#c0397b", "",        "Daughter / Niece"),
    ("#bbb",    "#f7f7f7", "Divorced"),
    ("#b0b0b0", "dotted",  "To research"),
]


def render_card(p):
    side_cls = f" {p['side']}-side" if p.get("side") else ""
    extra = " ".join(p.get("css", []))
    classes = f"card{(' ' + extra) if extra else ''}{side_cls}"
    lines = [f'<div class="{classes}" id="{p["id"]}">']
    lines.append(f'  <div class="name">{p["name"]}</div>')
    if p.get("maiden"):
        lines.append(f'  <div class="maiden">{p["maiden"]}</div>')
    if p.get("dob"):
        lines.append(f'  <div class="dob">{p["dob"]}</div>')
    if p.get("note"):
        lines.append(f'  <div class="note">{p["note"]}</div>')
    if p.get("tag"):
        lines.append(f'  <span class="tag">{p["tag"]}</span>')
    lines.append("</div>")
    return "\n".join("      " + l for l in lines)


def render_couple(people, side=None):
    side_cls = f" {side}-side" if side else ""
    out = [f'    <div class="couple{side_cls}">']
    for i, p in enumerate(people):
        out.append(render_card(p))
        if i < len(people) - 1:
            out.append('      <span class="heart">♥</span>')
    out.append("    </div>")
    return "\n".join(out)


def render_row(row_data, label, row_id):
    lines = [f'  <p class="gen-label">{label}</p>',
             f'  <div class="gen-row" id="{row_id}">']
    last_side = None
    for entry in row_data:
        kind, data = entry
        if kind in ("zitt", "zitt_single") and last_side in ("perez", "perez_single"):
            lines.append('    <div class="fam-gap"></div>')
        if kind in ("perez", "zitt") or (kind is None and isinstance(data, list)):
            side = "perez" if kind == "perez" else ("zitt" if kind == "zitt" else None)
            lines.append(render_couple(data, side=side))
        elif kind in ("perez_single", "zitt_single") or (kind is None and isinstance(data, dict)):
            side = "perez" if kind == "perez_single" else ("zitt" if kind == "zitt_single" else None)
            p = dict(data)
            p["side"] = side
            lines.append(render_card(p))
        last_side = kind
    lines.append("  </div>")
    return "\n".join(lines)


def render_legend():
    items = []
    for color, bg, label in LEGEND_ITEMS:
        style = f"border-color:{color};"
        if bg and bg not in ("", "dashed", "dotted"):
            style += f"background:{bg};"
        if bg in ("dashed", "dotted"):
            style += f"border-style:{bg};"
        items.append(
            f'  <div class="legend-item">'
            f'<div class="legend-box" style="{style}"></div>'
            f'<span>{label}</span></div>'
        )
    return '<div id="legend">\n' + "\n".join(items) + "\n</div>"


def generate_html():
    grandparents_html = render_row(
        [(side, list(pair)) for side, pair in GRANDPARENTS],
        "Grandparents", "row-gp"
    )
    parents_html = render_row(PARENTS, "Parents &amp; Aunt / Uncle Generation", "row-parents")
    gen3_html    = render_row(GEN3,    "Juan &amp; Melissa's Generation",        "row-gen3")
    kids_html    = render_row(KIDS,    "Children &amp; Next Generation",         "row-kids")

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>{HEADER['title']}</title>
  <style>
{CSS}
  </style>
</head>
<body>

<header>
  <h1>🌳 {HEADER['title']}</h1>
  <p>{HEADER['subtitle']}</p>
</header>

<div class=\"toggle-bar\">
  <button id=\"btn-all\"   onclick=\"setMode('all')\"   class=\"active\">🌳 Full Family Tree</button>
  <button id=\"btn-perez\" onclick=\"setMode('perez')\">🏠 Perez Family Only</button>
  <button id=\"btn-zitt\"  onclick=\"setMode('zitt')\"  class=\"zitt-btn\">🏠 Zitt · Coppola Family Only</button>
</div>

<div class=\"banner-row\">
  <span class=\"side-banner perez perez-side\">⬅ Perez · Santana Family</span>
  <span style=\"font-size:0.72em;color:#aaa;font-style:italic;\">← families join at Juan &amp; Melissa →</span>
  <span class=\"side-banner zitt zitt-side\">Zitt · Coppola Family ➡</span>
</div>

<div id=\"tree-scroll\">
<div id=\"tree\">
  <svg id=\"svg-lines\"></svg>

{grandparents_html}

{parents_html}

{gen3_html}

{kids_html}

</div>
</div>

{render_legend()}

<script>
{JS}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    html = generate_html()
    out_path = Path("index.html")
    out_path.write_text(html, encoding="utf-8")
    print(f"✅  Written {len(html):,} chars → {out_path.resolve()}")

    if "--preview" in sys.argv:
        import webbrowser
        webbrowser.open(str(out_path.resolve()))
