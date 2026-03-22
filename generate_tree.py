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

# Each person is a dict with keys:
#   id        – unique HTML id (required)
#   name      – display name
#   maiden    – maiden / alt name (optional)
#   dob       – date of birth string (optional)
#   note      – small italic note (optional)
#   tag       – relationship label (optional)
#   css       – extra CSS classes beyond "card" (optional, list)
#   side      – "perez" | "zitt" | None  → adds perez-side / zitt-side class

def person(id, name, maiden=None, dob=None, note=None, tag=None, css=None, side=None):
    return dict(id=id, name=name, maiden=maiden, dob=dob,
                note=note, tag=tag, css=css or [], side=side)

# ── Great-Grandparents ───────────────────────────────────────────

GREAT_GRANDPARENTS = [
    # Zoila's parents: Miguel Dalda + Ana Martinez (and Ana's siblings)
    ("perez", [
        person("miguel-dalda",    "Miguel Dalda",  dob="b. Unknown", tag="Great-Grandfather"),
        person("ana-martinez-gg", "Ana Martinez",  dob="b. Unknown", tag="Great-Grandmother"),
    ]),
    ("perez", [
        person("delia-martinez", "Delia Martinez",    dob="b. Unknown", tag="Grand-Aunt"),
        person("felix-hermida",  "Felix Hermida",     dob="b. Unknown",
               tag="Grand-Uncle-in-law", css=["in-law"]),
    ]),
    ("perez", [
        person("rosa-martinez",     "Rosa Martinez",     dob="b. Unknown", tag="Grand-Aunt"),
        person("guillermo-herrera", "Guillermo Herrera", dob="b. Unknown",
               tag="Grand-Uncle-in-law", css=["in-law"]),
    ]),
    ("perez_single", person("ramon-martinez", "Ramon Martinez", dob="b. Unknown", tag="Grand-Uncle")),
    # Miguel Dalda's sisters
    ("perez_single", person("zoraida-dalda",     "Zoraida Dalda",     dob="b. Unknown", tag="Grand-Aunt")),
    ("perez_single", person("maria-luisa-dalda", "Maria Luisa Dalda", dob="b. Unknown", tag="Grand-Aunt")),
    # Evaristo's parents: Lucas Santana + Maria Rangel (and Lucas's sisters)
    ("perez", [
        person("lucas-santana", "Lucas Santana", dob="b. Unknown", tag="Great-Grandfather"),
        person("maria-rangel",  "Maria Rangel",  dob="b. Unknown", tag="Great-Grandmother"),
    ]),
    ("perez_single", person("guillermina-santana", "Guillermina Santana", dob="b. Unknown", tag="Grand-Aunt")),
    ("perez_single", person("ramona-santana",      "Ramona Santana",     dob="b. Unknown", tag="Grand-Aunt")),
]

# ── Grandparents (+ their siblings) ─────────────────────────────

GRANDPARENTS = [
    # Perez side
    ("perez", [
        person("gp-gonzalo", "Gonzalo Perez", dob="b. Unknown", tag="Grandfather"),
        person("gp-osiris",  "Osiris Perez",  maiden="née Ramos", dob="b. Unknown", tag="Grandmother"),
    ]),
    # Santana/Dalda: Evaristo + Zolia + their siblings
    ("perez", [
        person("gp-evaristo", "Evaristo Santana", dob="b. Unknown", tag="Grandfather"),
        person("gp-zolia",    "Zolia Santana",    maiden="née Dalda", dob="b. Unknown", tag="Grandmother"),
    ]),
    ("perez", [
        person("ana-luisa-dalda", "Ana Luisa Dalda", dob="b. Unknown", tag="Grand-Aunt"),
        person("manolo-fundora",  "Manolo Fundora",  dob="b. Unknown",
               tag="Grand-Uncle-in-law", css=["in-law"]),
    ]),
    ("perez", [
        person("gerardo-dalda", "Gerardo Dalda", dob="b. Unknown", tag="Grand-Uncle"),
        person("elisa-gorrin",  "Elisa Gorrin",  dob="b. Unknown",
               tag="Grand-Aunt-in-law", css=["in-law"]),
    ]),
    ("perez_single", person("juan-santana-bro", "Juan Santana",  dob="b. Unknown", tag="Grand-Uncle")),
    ("perez_single", person("juana-santana",    "Juana Santana", dob="b. Unknown", tag="Grand-Aunt")),
    # Zitt side
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

# ── Parents generation ────────────────────────────────────────────

PARENTS = [
    # Aunt + uncle (perez side)
    ("perez", [
        person("ana-osiris",  "Ana Osiris Martinez", maiden="née Perez", dob="b. Unknown",
               tag="Aunt (Paternal)", css=["cousin"]),
        person("antonio-sr",  "Antonio Martinez",   dob="b. Unknown", tag="Uncle", css=["cousin"]),
    ]),
    # Juan's parents
    ("perez", [
        person("father", "Juan Gonzalo Perez", dob="b. June 11, 1955", tag="Father"),
        person("mother", "Zaida Perez", maiden="née Santana", dob="b. Sep 13, 1957", tag="Mother"),
    ]),
    # Stepmother + Dayanna's father (singles, perez side)
    ("perez_single", person("olga", "Olga", dob="b. Unknown", tag="Stepmother", css=["unknown"])),
    ("perez_single", person("dayanna-father", "Unknown Father", dob="b. Unknown",
                            tag="Dayanna's Father", css=["unknown"])),
    # Melissa's parents (zitt side)
    ("zitt", [
        person("dennis-zitt", "Dennis Herbert Zitt", dob="b. Apr 27, 1949",
               tag="Father-in-law", css=["zitt"]),
        person("anna-zitt",   "Anna Louise Zitt", maiden="née Coppola", dob="b. Mar 25, 1952",
               tag="Mother-in-law", css=["zitt"]),
    ]),
]

# ── Juan & Melissa's generation ───────────────────────────────────

GEN3 = [
    # Martinez cousins
    ("perez_single", person("antonio-jr", "Antonio Martinez", dob="b. Unknown",
                            tag="Cousin", css=["cousin"])),
    ("perez", [
        person("ana-martinez",   "Ana Margarita Ramirez", maiden="née Martinez", dob="b. Unknown",
               tag="Cousin", css=["cousin"]),
        person("daniel-ramirez", "Daniel Ramirez", dob="b. Unknown",
               tag="Cousin-in-law", css=["cousin"]),
    ]),
    # Gonzalo (single)
    ("perez_single", person("gonzalo", "Gonzalo E. Perez", dob="b. July 27, 1976", tag="Brother")),
    # THE COUPLE — no side filter (always visible)
    (None, [
        person("juan",    "Juan Miguel Perez", dob="b. Oct 28, 1980", tag="You",    css=["you"]),
        person("melissa", "Melissa Perez", maiden="née Zitt", dob="b. Mar 15, 1981",
               tag="Spouse", css=["spouse"]),
    ]),
    # Daniel + Jennifer
    ("perez", [
        person("daniel",   "Daniel Orlando Perez", dob="b. June 23, 1982", tag="Brother"),
        person("jennifer", "Jennifer Perez", maiden="née Safanova",
               tag="Sister-in-law", css=["in-law"]),
    ]),
    # Half-siblings
    ("perez_single", person("joanna",  "Joanna Marie Perez", dob="b. 2005", tag="Half-Sister",  css=["half"])),
    ("perez_single", person("dayanna", "Dayanna", maiden="Last name TBD",
                            note="Olga's daughter (diff. father)",
                            tag="Joanna's Half-Sister", css=["half"])),
    # Zitt siblings
    ("zitt_single", person("deanna", "Deanna Marie Lebet", maiden="née Zitt", dob="b. Aug 13, 1969",
                           tag="Sister-in-law", css=["zitt-sib"])),
    ("zitt", [
        person("patricia",       "Patricia Ann Welton", maiden="née Zitt", dob="b. June 12, 1971",
               tag="Sister-in-law", css=["zitt-sib"]),
        person("michael-welton", "Michael Welton", tag="Brother-in-law", css=["in-law"]),
    ]),
    ("zitt_single", person("dennis-wayne", "Dennis Wayne Zitt", dob="b. June 14, 1974",
                           note="Divorced · No children",
                           tag="Brother-in-law", css=["zitt-sib"])),
]

# ── Children / next generation ────────────────────────────────────

KIDS = [
    # Ramirez 2nd cousins
    ("perez_single", person("melenia",   "Melenia Ramirez",    dob="b. Unknown", tag="2nd Cousin", css=["cousin"])),
    ("perez_single", person("alejandro", "Alejandro Ramirez",  dob="b. Unknown", tag="2nd Cousin", css=["cousin"])),
    ("perez_single", person("mya",       "Mya Ramirez",        dob="b. Unknown", tag="2nd Cousin", css=["cousin"])),
    ("perez_single", person("alexandria","Alexandria Ramirez",  dob="b. Unknown", tag="2nd Cousin", css=["cousin"])),
    ("perez_single", person("jamila",    "Jamila Ramirez", dob="b. Unknown",
                            note="Mother unknown", tag="2nd Cousin", css=["cousin"])),
    # Juan + Melissa's children — no side (always visible)
    (None,           person("julian", "Julian Lucas Perez",  dob="b. Feb 4, 2011",  tag="Son",      css=["child-m"])),
    (None,           person("alexa",  "Alexa Santana Perez", dob="b. Feb 4, 2015",  tag="Daughter", css=["child-f"])),
    (None,           person("sophia", "Sophia Quinn Perez",  dob="b. Oct 4, 2022",  tag="Daughter", css=["child-f"])),
    # Daniel + Jennifer's daughter (perez side)
    ("perez_single", person("sena", "Sena Sakura Perez", dob="b. April 2014",
                            tag="Niece", css=["child-f"])),
    # Lebet children
    ("zitt_single",  person("john-lebet-jr", "John Lebet",    dob="b. Unknown", tag="Nephew",  css=["niece-m"])),
    ("zitt_single",  person("kevin-lebet",   "Kevin Lebet",   dob="b. Unknown", tag="Nephew",  css=["niece-m"])),
    ("zitt_single",  person("matthew-lebet", "Matthew Lebet", dob="b. Unknown", tag="Nephew",  css=["niece-m"])),
    ("zitt_single",  person("kaitlyn",       "Kaitlyn", maiden="Different father",
                            tag="Niece",  css=["niece-f"])),
    # Welton children
    ("zitt_single",  person("stephanie-welton", "Stephanie Welton", dob="b. Unknown", tag="Niece",   css=["niece-f"])),
    ("zitt_single",  person("brian-welton",     "Brian Welton",     dob="b. Unknown", tag="Nephew",  css=["niece-m"])),
]

# ── Grandparent cousins (children of grandparent siblings + great-GP siblings) ──

GP_COUSINS = [
    # Children of Delia Martinez + Felix Hermida
    ("perez_single", person("enerita-hermida", "Enerita Hermida", dob="b. Unknown", tag="Grand-Cousin")),
    ("perez_single", person("elisa-hermida",   "Elisa Hermida",   dob="b. Unknown", tag="Grand-Cousin")),
    ("perez_single", person("oreste-hermida",  "Oreste Hermida",  dob="b. Unknown", tag="Grand-Cousin")),
    # Children of Rosa Martinez + Guillermo Herrera
    ("perez_single", person("nilda-herrera", "Nilda Herrera", dob="b. Unknown", tag="Grand-Cousin")),
    ("perez_single", person("daizy-herrera", "Daizy Herrera", dob="b. Unknown", tag="Grand-Cousin")),
    ("perez_single", person("luis-herrera",  "Luis Herrera",  dob="b. Unknown", tag="Grand-Cousin")),
    # Children of Maria Luisa Dalda
    ("perez_single", person("maria-belen-dalda", "Maria Belen Dalda", dob="b. Unknown", tag="Grand-Cousin")),
    ("perez_single", person("guilfredo-dalda",   "Guilfredo Dalda",   dob="b. Unknown", tag="Grand-Cousin")),
    # Child of Ana Luisa Dalda + Manolo Fundora
    ("perez_single", person("ana-herminia-fundora", "Ana Herminia Fundora", dob="b. Unknown",
                             note="née Fundora", tag="Grand-Cousin")),
    # Children of Gerardo Dalda + Elisa Gorrin
    ("perez_single", person("belkys-dalda",  "Belkys Dalda",  dob="b. Unknown", tag="Grand-Cousin")),
    ("perez_single", person("idalmis-dalda", "Idalmis Dalda", dob="b. Unknown", tag="Grand-Cousin")),
    # Children of Juan Santana (Evaristo's brother)
    ("perez_single", person("nancy-santana",   "Nancy Santana",    dob="b. Unknown", tag="Grand-Cousin")),
    ("perez_single", person("juan-santana-jr", "Juan Santana Jr.", dob="b. Unknown", tag="Grand-Cousin")),
]

# ── SVG connector rules ───────────────────────────────────────────
# Each rule is a dict:
#   parents  – list of person ids forming the couple midpoint
#   children – list of child person ids
#   color    – CSS color string
#   dash     – bool (dashed line)
#   special  – "father-olga" | "olga-dayanna" (for offset connectors)

CONNECTORS = [
    dict(parents=["gp-gonzalo","gp-osiris"],   children=["ana-osiris","father"], color="C"),
    dict(parents=["gp-evaristo","gp-zolia"],   children=["mother"],              color="C"),
    dict(parents=["zp-gf","zp-gm"],            children=["dennis-zitt"],         color="BL", dash=True),
    dict(parents=["coppola-gf","coppola-gm"],  children=["anna-zitt"],           color="BL"),
    dict(parents=["father","mother"],           children=["gonzalo","juan","daniel"], color="C"),
    dict(special="father-olga",                children=["joanna"],              color="GR", dash=True),
    dict(special="olga-dayanna",               children=["dayanna"],             color="OR", dash=True),
    dict(parents=["ana-osiris","antonio-sr"],  children=["antonio-jr","ana-martinez"], color="PU"),
    dict(parents=["dennis-zitt","anna-zitt"],  children=["deanna","patricia","dennis-wayne","melissa"], color="BL"),
    dict(parents=["ana-martinez","daniel-ramirez"], children=["melenia","alejandro","mya","alexandria"], color="PU"),
    dict(special="ramirez-jamila",             children=["jamila"],              color="PU", dash=True),
    dict(parents=["daniel","jennifer"],        children=["sena"],                color="C"),
    dict(parents=["juan","melissa"],           children=["julian","alexa","sophia"], color="KB"),
    dict(parents=["deanna"],                   children=["john-lebet-jr","kevin-lebet","matthew-lebet"], color="BL"),
    dict(parents=["patricia","michael-welton"],children=["stephanie-welton","brian-welton"], color="BL"),
    dict(special="patricia-kaitlyn",           children=["kaitlyn"],             color="BL", dash=True),
    dict(parents=["miguel-dalda","ana-martinez-gg"],   children=["ana-luisa-dalda","gp-zolia","gerardo-dalda"], color="C"),
    dict(parents=["lucas-santana","maria-rangel"],      children=["gp-evaristo","juan-santana-bro","juana-santana"], color="C"),
    dict(parents=["delia-martinez","felix-hermida"],    children=["enerita-hermida","elisa-hermida","oreste-hermida"], color="C"),
    dict(parents=["rosa-martinez","guillermo-herrera"], children=["nilda-herrera","daizy-herrera","luis-herrera"], color="C"),
    dict(parents=["maria-luisa-dalda"],                 children=["maria-belen-dalda","guilfredo-dalda"], color="C"),
    dict(parents=["ana-luisa-dalda","manolo-fundora"],  children=["ana-herminia-fundora"], color="C"),
    dict(parents=["gerardo-dalda","elisa-gorrin"],      children=["belkys-dalda","idalmis-dalda"], color="C"),
    dict(parents=["juan-santana-bro"],                  children=["nancy-santana","juan-santana-jr"], color="C"),
]

# ══════════════════════════════════════════════════════════════════
#  HTML RENDERING  —  no need to edit below this line
# ══════════════════════════════════════════════════════════════════

CSS = """
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
      min-width: 5500px;
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
                   padding: 4px 12px; border-radius: 20px; display: inline-block; }
    .side-banner.perez { background: #f8ece0; color: #7d4e1e; border: 1px solid #d4b896; }
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

// ── Connector helpers ──
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

  // Gonzalo Perez + Osiris → father + ana-osiris
  const gpG=rel('gp-gonzalo'),gpO=rel('gp-osiris'),father=rel('father'),anaO=rel('ana-osiris');
  if(gpG&&gpO&&father&&anaO) tee(svg,(gpG.cx+gpO.cx)/2,Math.max(gpG.bottom,gpO.bottom),[anaO,father],C);

  // Evaristo + Zolia → mother
  const gpE=rel('gp-evaristo'),gpZ=rel('gp-zolia'),mother=rel('mother');
  if(gpE&&gpZ&&mother) tee(svg,(gpE.cx+gpZ.cx)/2,Math.max(gpE.bottom,gpZ.bottom),[mother],C);

  // Zitt GPs → Dennis Zitt
  const zpgf=rel('zp-gf'),zpgm=rel('zp-gm'),dZitt=rel('dennis-zitt');
  if(zpgf&&zpgm&&dZitt) tee(svg,(zpgf.cx+zpgm.cx)/2,Math.max(zpgf.bottom,zpgm.bottom),[dZitt],BL,true);

  // Coppola GPs → Anna Zitt
  const cgf=rel('coppola-gf'),cgm=rel('coppola-gm'),aZitt=rel('anna-zitt');
  if(cgf&&cgm&&aZitt) tee(svg,(cgf.cx+cgm.cx)/2,Math.max(cgf.bottom,cgm.bottom),[aZitt],BL);

  // Father + Mother → Gonzalo, Juan, Daniel
  const gonzalo=rel('gonzalo'),juan=rel('juan'),daniel=rel('daniel');
  if(father&&mother&&gonzalo&&juan&&daniel)
    tee(svg,(father.right+mother.left)/2,Math.max(father.bottom,mother.bottom),[gonzalo,juan,daniel],C);
  else if(father&&mother&&juan)
    tee(svg,(father.right+mother.left)/2,Math.max(father.bottom,mother.bottom),[juan],C);

  // Father + Olga → Joanna
  const olga=rel('olga'),joanna=rel('joanna');
  if(father&&olga&&joanna){
    const ux=(father.cx+olga.cx)/2,fBy=father.bottom;
    ln(svg,father.cx,fBy,father.cx,fBy+14,GR,true);
    ln(svg,father.cx,fBy+14,ux,fBy+14,GR,true);
    ln(svg,ux,fBy+14,ux,olga.bottom,GR,true);
    tee(svg,ux,olga.bottom,[joanna],GR,true);
  }

  // Olga + Unknown → Dayanna
  const dayF=rel('dayanna-father'),dayanna=rel('dayanna');
  if(olga&&dayF&&dayanna){
    const ux=(olga.cx+dayF.cx)/2,oBy=olga.bottom;
    ln(svg,olga.cx,oBy,olga.cx,oBy+14,OR,true);
    ln(svg,olga.cx,oBy+14,ux,oBy+14,OR,true);
    ln(svg,ux,oBy+14,ux,Math.max(olga.bottom,dayF.bottom),OR,true);
    tee(svg,ux,Math.max(olga.bottom,dayF.bottom),[dayanna],OR,true);
  }

  // Ana Osiris + Antonio → cousins
  const antJr=rel('antonio-jr'),anaMtz=rel('ana-martinez'),antSr=rel('antonio-sr');
  if(anaO&&antSr&&antJr&&anaMtz)
    tee(svg,(anaO.right+antSr.left)/2,Math.max(anaO.bottom,antSr.bottom),[antJr,anaMtz],PU);

  // Dennis Zitt + Anna → Deanna, Patricia, Dennis Wayne, Melissa
  const deanna=rel('deanna'),patricia=rel('patricia'),dWayne=rel('dennis-wayne'),melissa=rel('melissa');
  if(dZitt&&aZitt&&melissa){
    const kids=[deanna,patricia,dWayne,melissa].filter(Boolean);
    tee(svg,(dZitt.right+aZitt.left)/2,Math.max(dZitt.bottom,aZitt.bottom),kids,BL);
  }

  // Ana Martinez + Daniel Ramirez → Melenia, Alejandro, Mya, Alexandria
  const dRam=rel('daniel-ramirez'),anaMart=rel('ana-martinez');
  const mel=rel('melenia'),ale=rel('alejandro'),mya2=rel('mya'),alex=rel('alexandria');
  if(anaMart&&dRam&&mel) tee(svg,(anaMart.right+dRam.left)/2,Math.max(anaMart.bottom,dRam.bottom),[mel,ale,mya2,alex].filter(Boolean),PU);

  // Daniel Ramirez → Jamila (dashed)
  const jamila=rel('jamila');
  if(dRam&&jamila){
    const midY=dRam.bottom+(jamila.top-dRam.bottom)*0.5;
    ln(svg,dRam.cx,dRam.bottom,dRam.cx,midY,PU,true);
    ln(svg,dRam.cx,midY,jamila.cx,midY,PU,true);
    ln(svg,jamila.cx,midY,jamila.cx,jamila.top,PU,true);
  }

  // Daniel + Jennifer → Sena
  const danP=rel('daniel'),jennifer=rel('jennifer'),sena=rel('sena');
  if(danP&&jennifer&&sena) tee(svg,(danP.right+jennifer.left)/2,Math.max(danP.bottom,jennifer.bottom),[sena],C);

  // Juan + Melissa → Julian, Alexa, Sophia
  const juanR=rel('juan'),melissaR=rel('melissa'),jul=rel('julian'),alx=rel('alexa'),soph=rel('sophia');
  if(juanR&&melissaR&&jul)
    tee(svg,(juanR.right+melissaR.left)/2,Math.max(juanR.bottom,melissaR.bottom),[jul,alx,soph].filter(Boolean),KB);

  // Deanna → John Jr., Kevin, Matthew
  const jJr=rel('john-lebet-jr'),kev=rel('kevin-lebet'),matt=rel('matthew-lebet');
  if(deanna&&jJr) tee(svg,deanna.cx,deanna.bottom,[jJr,kev,matt].filter(Boolean),BL);

  // Patricia + Michael Welton → Stephanie, Brian
  const mWelton=rel('michael-welton'),steph=rel('stephanie-welton'),brian=rel('brian-welton');
  if(patricia&&mWelton&&steph) tee(svg,(patricia.right+mWelton.left)/2,Math.max(patricia.bottom,mWelton.bottom),[steph,brian].filter(Boolean),BL);

  // Patricia → Kaitlyn (dashed, diff father)
  const kaitlyn=rel('kaitlyn');
  if(patricia&&kaitlyn){
    const midY=patricia.bottom+(kaitlyn.top-patricia.bottom)*0.5;
    ln(svg,patricia.cx,patricia.bottom,patricia.cx,midY,BL,true);
    ln(svg,patricia.cx,midY,kaitlyn.cx,midY,BL,true);
    ln(svg,kaitlyn.cx,midY,kaitlyn.cx,kaitlyn.top,BL,true);
  }

  // Miguel Dalda + Ana Martinez → Zoila's generation
  const migD=rel('miguel-dalda'),anaMG=rel('ana-martinez-gg'),anaLD=rel('ana-luisa-dalda'),gerD=rel('gerardo-dalda');
  const zoliGP=rel('gp-zolia');
  if(migD&&anaMG&&zoliGP) tee(svg,(migD.right+anaMG.left)/2,Math.max(migD.bottom,anaMG.bottom),[anaLD,zoliGP,gerD].filter(Boolean),C);

  // Lucas Santana + Maria Rangel → Evaristo's generation
  const lucS=rel('lucas-santana'),marR=rel('maria-rangel'),evGP=rel('gp-evaristo');
  const juanSB=rel('juan-santana-bro'),juanaS=rel('juana-santana');
  if(lucS&&marR&&evGP) tee(svg,(lucS.right+marR.left)/2,Math.max(lucS.bottom,marR.bottom),[evGP,juanSB,juanaS].filter(Boolean),C);

  // Delia + Felix Hermida → Enerita, Elisa, Oreste
  const delM=rel('delia-martinez'),felH=rel('felix-hermida');
  const enH=rel('enerita-hermida'),elH=rel('elisa-hermida'),orH=rel('oreste-hermida');
  if(delM&&felH&&enH) tee(svg,(delM.right+felH.left)/2,Math.max(delM.bottom,felH.bottom),[enH,elH,orH].filter(Boolean),C);

  // Rosa + Guillermo Herrera → Nilda, Daizy, Luis
  const rosaM=rel('rosa-martinez'),guilH=rel('guillermo-herrera');
  const nildH=rel('nilda-herrera'),daizH=rel('daizy-herrera'),luisH=rel('luis-herrera');
  if(rosaM&&guilH&&nildH) tee(svg,(rosaM.right+guilH.left)/2,Math.max(rosaM.bottom,guilH.bottom),[nildH,daizH,luisH].filter(Boolean),C);

  // Maria Luisa Dalda → Maria Belen, Guilfredo
  const mlD=rel('maria-luisa-dalda'),mbD=rel('maria-belen-dalda'),gfD=rel('guilfredo-dalda');
  if(mlD&&mbD) tee(svg,mlD.cx,mlD.bottom,[mbD,gfD].filter(Boolean),C);

  // Ana Luisa + Manolo Fundora → Ana Herminia
  const manoF=rel('manolo-fundora'),anaHF=rel('ana-herminia-fundora');
  if(anaLD&&manoF&&anaHF) tee(svg,(anaLD.right+manoF.left)/2,Math.max(anaLD.bottom,manoF.bottom),[anaHF],C);

  // Gerardo + Elisa Gorrin → Belkys, Idalmis
  const elisaG=rel('elisa-gorrin'),belkD=rel('belkys-dalda'),idalD=rel('idalmis-dalda');
  if(gerD&&elisaG&&belkD) tee(svg,(gerD.right+elisaG.left)/2,Math.max(gerD.bottom,elisaG.bottom),[belkD,idalD].filter(Boolean),C);

  // Juan Santana (Evaristo's brother) → Nancy, Juan Jr.
  const juanSBr=rel('juan-santana-bro'),nancS=rel('nancy-santana'),juanSJr=rel('juan-santana-jr');
  if(juanSBr&&nancS) tee(svg,juanSBr.cx,juanSBr.bottom,[nancS,juanSJr].filter(Boolean),C);
}

window.addEventListener('load', draw);
window.addEventListener('resize', draw);
"""

LEGEND_ITEMS = [
    ("#c0392b", "",       "You"),
    ("#d4b896", "",       "Perez family"),
    ("#7d3c98", "dashed", "Spouse"),
    ("#6c3483", "#fdf2ff","Cousin branch"),
    ("#2471a3", "#f0f6fc","Zitt family"),
    ("#1e8449", "dashed", "Half-sibling"),
    ("#2980b9", "",       "Son / Nephew"),
    ("#c0397b", "",       "Daughter / Niece"),
    ("#bbb",    "#f7f7f7","Divorced"),
    ("#b0b0b0", "dotted", "To research"),
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
        # Insert separators between sides
        if kind in ("zitt", "zitt_single") and last_side in ("perez", "perez_single"):
            lines.append('    <div class="fam-gap"></div>')
        elif kind in ("perez", "perez_single") and last_side == "zitt":
            pass  # shouldn't happen normally

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
    gg_html          = render_row(GREAT_GRANDPARENTS, "Great-Grandparents &amp; Their Siblings", "row-gg")
    grandparents_html = render_row(GRANDPARENTS, "Grandparents &amp; Their Siblings", "row-gp")
    gp_cousins_html  = render_row(GP_COUSINS,   "Grandparent Generation Cousins",    "row-gp-cousins")
    parents_html     = render_row(PARENTS, "Parents &amp; Aunt / Uncle Generation",  "row-parents")
    gen3_html        = render_row(GEN3,    "Juan &amp; Melissa's Generation",         "row-gen3")
    kids_html        = render_row(KIDS,    "Children &amp; Next Generation",          "row-kids")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
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

<div class="toggle-bar">
  <button id="btn-all"   onclick="setMode('all')"   class="active">🌳 Full Family Tree</button>
  <button id="btn-perez" onclick="setMode('perez')">🏠 Perez Family Only</button>
  <button id="btn-zitt"  onclick="setMode('zitt')"  class="zitt-btn">🏠 Zitt · Coppola Family Only</button>
</div>

<div class="banner-row">
  <span class="side-banner perez perez-side">⬅ Perez · Santana Family</span>
  <span style="font-size:0.72em;color:#aaa;font-style:italic;">← families join at Juan &amp; Melissa →</span>
  <span class="side-banner zitt zitt-side">Zitt · Coppola Family ➡</span>
</div>

<div id="tree-scroll">
<div id="tree">
  <svg id="svg-lines"></svg>

{gg_html}

{grandparents_html}

{gp_cousins_html}

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
