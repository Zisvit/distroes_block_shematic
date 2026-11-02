#!/usr/bin/env python3
"""Вставляет белый скруглённый rect под каждую подпись ребра (xlabel) в SVG Graphviz,
чтобы линии не пересекали текст. Работает только внутри <g id="edge...">."""

import re, sys

SRC, DST = "flowchart.svg", "flowchart.svg"
s = open(SRC, encoding="utf-8").read()

FACTOR, PADX = 0.65, 7  # ширина символа в em + поля


def patch_edge(m):
    g = m.group(0)

    def patch_text(t):
        attrs, body = t.group(2), t.group(3)
        x = float(re.search(r'x="([\d.\-]+)"', attrs).group(1))
        y = float(re.search(r'y="([\d.\-]+)"', attrs).group(1))
        size = float(re.search(r'font-size="([\d.]+)"', attrs).group(1))
        txt = re.sub(r"&(#\d+|\w+);", "X", body)  # entity ~ 1 символ
        w = len(txt) * size * FACTOR + PADX * 2
        h = size * 1.35
        rx = size * 0.4
        rect = (
            f'<rect x="{x - w / 2:.2f}" y="{y - size * 1.02:.2f}" width="{w:.2f}" '
            f'height="{h:.2f}" rx="{rx:.2f}" fill="white"/>'
        )
        return rect + t.group(0)

    return re.sub(r"(<text\b([^>]*)>(.*?)</text>)", patch_text, g, flags=re.S)


s2, n = re.subn(r'(<g id="edge[^>]*>.*?</g>)', patch_edge, s, flags=re.S)
open(DST, "w", encoding="utf-8").write(s2)
ntext = len(re.findall(r'<g id="edge', s2))
print(f"групп edge: {ntext}, пропатчено групп: {n}, файл: {DST}, размер: {len(s2)}")
