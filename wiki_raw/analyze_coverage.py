#!/usr/bin/env python3
"""Сверяет покрытие схемы с именами из Википедии. Печатает непокрытое."""

import json, re

DOT = "flowchart.dot"
dot = open(DOT, encoding="utf-8").read()


def norm(s):
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


# Все тексты меток из DOT (имена + стереотипы — для сверки берём всё)
covered_raw = set()
for m in re.finditer(r'label="((?:[^"\\]|\\.)*)"', dot):
    txt = m.group(1).replace("\\n", " ")
    # режем стереотип в кавычках-ёлочках: имя обычно до «...»
    head = txt.split("«")[0]
    for part in re.split(r"[/|]", head):
        p = part.strip(" .")
        if p and len(p) > 1 and not p.startswith(("ВЕТКА", "Легенда")):
            covered_raw.add(p)
covered = {norm(c) for c in covered_raw}


def norm_name(n):
    n = norm(n)
    n = re.sub(
        r"\s+(linux|gnu\/linux|os|system|distribution|project|edition)(\s|$)", " ", n
    )
    n = re.sub(r"^(gnu|the)\s+", "", n)
    return n.strip()


cov_n = {norm_name(c) for c in covered_raw}

d = json.load(open("wiki_raw/distros.json", encoding="utf-8"))
report = []
total_wiki, miss_wiki = 0, []
for art in ["List of Linux distributions", "List of BSD operating systems"]:
    for fam, names in d[art].items():
        for n in names:
            total_wiki += 1
            nn = norm_name(n)
            hit = nn in cov_n or any(nn in c or c in nn for c in cov_n if len(nn) > 3)
            if not hit:
                miss_wiki.append((fam, n))
report.append(f"WIKI: всего {total_wiki}, не покрыто {len(miss_wiki)}")
for fam, n in miss_wiki:
    report.append(f"  MISS [{fam}] {n}")

tl = d.get("__timeline_labels__", [])
junk = re.compile(
    r"^[vV]?\d+(\.\d+)+$|^\d+\s?(mb|gb|kb)$|independent|based|desktop|server|live|rolling|stable|testing|based on",
    re.I,
)
miss_tl = []
for t in tl:
    if junk.search(t) or len(t) < 2:
        continue
    nn = norm_name(t)
    if nn not in cov_n and not any((nn in c or c in nn) for c in cov_n if len(nn) > 3):
        miss_tl.append(t)
report.append(f"TIMELINE: меток {len(tl)}, непокрытых {len(miss_tl)}")
for t in sorted(set(miss_tl)):
    report.append(f"  TL-MISS {t}")

open("wiki_raw/coverage_report.txt", "w").write("\n".join(report))
print("\n".join(report[:200]))
print("...")
print(f"(полный отчёт: wiki_raw/coverage_report.txt, строк: {len(report)})")
