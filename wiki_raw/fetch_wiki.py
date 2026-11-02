#!/usr/bin/env python3
"""Скачивает списки ОС/дистрибутивов из Википедии и складывает в wiki_raw/distros.json"""

import json, re, sys, urllib.request, urllib.parse, os, html

UA = {"User-Agent": "distro-chart-bot/1.0 (educational flowchart)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wiki_raw")
os.makedirs(OUT, exist_ok=True)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=60).read()


def wikitext(title, site="en.wikipedia.org"):
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "prop": "revisions",
            "rvprop": "content",
            "rvslots": "main",
            "titles": title,
        }
    )
    data = json.loads(get(f"https://{site}/w/api.php?{q}"))
    return data["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]


SKIP_NS = (
    "File:",
    "Image:",
    "Category:",
    "Template:",
    "Wikipedia:",
    "Help:",
    "Portal:",
    "Draft:",
    "Module:",
    "MediaWiki:",
    "TimedText:",
)


def parse_tables(wt):
    """Возвращает {family: [names]} — первое [[...]] в каждой строке-ячейке таблицы."""
    fams, cur = {}, ["ROOT"]
    row_first_cell = None
    for line in wt.splitlines():
        m = re.match(r"^(=+)\s*(.+?)\s*\1\s*$", line)
        if m:
            level = len(m.group(1))
            name = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            cur = cur[: level - 2] + [name] if level >= 2 else [name]
            continue
        if line.startswith("|-"):
            row_first_cell = True
            continue
        if row_first_cell and re.match(r"^\|[^|]", line):
            row_first_cell = False
            mm = re.search(r"\[\[([^|\]#]+)(?:\|([^]]+))?\]\]", line)
            if mm:
                page, disp = mm.group(1).strip(), (mm.group(2) or mm.group(1)).strip()
                if not page.startswith(SKIP_NS) and len(disp) > 1:
                    fam = " / ".join(cur)
                    fams.setdefault(fam, [])
                    if disp not in fams[fam]:
                        fams[fam].append(disp)
    return fams


result = {}
for title in [
    "List of Linux distributions",
    "List of BSD operating systems",
    "List of operating systems",
]:
    try:
        wt = wikitext(title)
        open(os.path.join(OUT, title.replace(" ", "_") + ".wiki.txt"), "w").write(wt)
        fams = parse_tables(wt)
        result[title] = fams
        n = sum(len(v) for v in fams.values())
        print(f"{title}: {len(fams)} разделов, {n} имён")
    except Exception as e:
        print(f"{title}: ОШИБКА {e}", file=sys.stderr)

# --- Таймлайн с Commons (та самая «превосходная фотография») ---
try:
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "list": "search",
            "srsearch": "Linux Distribution Timeline",
            "srnamespace": "6",
            "srlimit": "20",
        }
    )
    data = json.loads(get(f"https://commons.wikimedia.org/w/api.php?{q}"))
    cands = [r["title"] for r in data["query"]["search"]]
    svg_title = next((t for t in cands if t.lower().endswith(".svg")), cands[0])
    print("timeline file:", svg_title)
    q2 = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "prop": "imageinfo",
            "iiprop": "url|size",
            "titles": svg_title,
        }
    )
    info = json.loads(get(f"https://commons.wikimedia.org/w/api.php?{q2}"))
    page = info["query"]["pages"][0]
    url = page["imageinfo"][0]["url"]
    print("timeline url:", url, page["imageinfo"][0].get("size"))
    svg = get(url).decode("utf-8", "replace")
    open(os.path.join(OUT, "timeline.svg"), "w").write(svg)
    texts = re.findall(r"<text[^>]*>(.*?)</text>", svg, re.S)
    names = set()
    for t in texts:
        t = html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
        t = re.sub(r"\s+", " ", t)
        if re.fullmatch(r"[12][0-9]{3}([.‒–-][0-9xX.]*)?", t):
            continue  # годы
        if 1 < len(t) < 40 and not t.startswith(("http", "www")):
            names.add(t)
    tl = sorted(names)
    print(f"timeline: {len(tl)} текстовых меток")
    result["__timeline_labels__"] = tl
except Exception as e:
    print(f"timeline: ОШИБКА {e}", file=sys.stderr)

json.dump(
    result, open(os.path.join(OUT, "distros.json"), "w"), ensure_ascii=False, indent=1
)
flat = set()
for k, v in result.items():
    if k.startswith("__"):
        flat.update(v)
    elif isinstance(v, dict):
        for names in v.values():
            flat.update(names)
print("ИТОГО уникальных имён:", len(flat))
