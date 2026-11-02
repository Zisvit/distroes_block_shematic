<p align="center">
  <img src="banner.svg" alt="ОС-Блок-схема" width="100%"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/blocks-198-00f5a0?style=for-the-badge" alt="blocks"/>
  <img src="https://img.shields.io/badge/diamonds-37-00d9f5?style=for-the-badge" alt="diamonds"/>
  <img src="https://img.shields.io/badge/names-~490-a855f7?style=for-the-badge" alt="names"/>
  <img src="https://img.shields.io/badge/coverage-92%25-f59e0b?style=for-the-badge" alt="coverage"/>
  <img src="https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge" alt="license"/>
</p>

<p align="center">
  <a href="flowchart.svg"><b>Основная схема (SVG)</b></a> ·
  <a href="flowchart.png"><b>PNG</b></a> ·
  <a href="flowchart.pdf"><b>PDF</b></a> ·
  <a href="flowchart_simple.svg"><b>Упрощённая (SVG)</b></a> ·
  <a href="flowchart_simple.png"><b>PNG</b></a> ·
  <a href="flowchart_simple.pdf"><b>PDF</b></a> ·
  <a href="flowchart.mmd"><b>Mermaid</b></a> ·
  <a href="flowchart.dot"><b>Graphviz</b></a>
</p>

<details>
<summary><b>🎬 Мини-превью графа (Mermaid)</b></summary>

```mermaid
flowchart TD
  START([СТАРТ]) --> G{Играешь в AAA?}
  G -- да --> GAMING[🎮 Гейминг: Windows 11, Bazzite, SteamOS...]
  G -- нет --> H{ПК слабый?}
  H -- да --> HW[♻️ Воскрешение железа: antiX, Puppy, Alpine...]
  H -- нет --> S{Сервер / NAS?}
  S -- да --> SRV[🖥️ Серверы: Proxmox, TrueNAS, OpenWrt...]
  S -- нет --> P{Анонимность / пентест?}
  P -- да --> PRIV[🕵️ Приватность: Tails, Qubes, Kali...]
  P -- нет --> FIN([ФИНИШ])
  style START fill:#111,color:#fff
  style FIN fill:#111,color:#fff
  style G fill:#f59e0b,color:#000
  style H fill:#f59e0b,color:#000
  style S fill:#f59e0b,color:#000
  style P fill:#f59e0b,color:#000
```

</details>

---

# Блок-схема «Какую ОС ставить?» — if/else по дистрибутивам

Классическая блок-схема выбора операционной системы: старт → цепочка ромбов `if/else` → прямоугольник с дистрибутивом. 

**Масштаб: 198 блоков-ответов, 37 ромбов-вопросов, ~490 названий систем.**

## Файлы

| Файл | Что это |
|---|---|
| `flowchart.svg` | **Основная схема.** Дерево принятия решений с if/else. Вектор, зум без потери качества. |
| `flowchart.png` | Растр основной схемы |
| `flowchart.pdf` | Вектор основной схемы для печати |
| `flowchart_simple.svg` | **Упрощённая схема.** Популярные дистрибутивы по сферам с if/else логикой. |
| `flowchart_simple.png` | Растр упрощённой схемы |
| `flowchart_simple.pdf` | Вектор упрощённой схемы для печати |
| `flowchart.dot` | Исходник Graphviz основной схемы |
| `flowchart.mmd` | Mermaid-версия для GitHub, Notion, Obsidian |
| `banner.svg` | Анимированный баннер |
| `wiki_raw/` | Данные из Википедии + скрипты сбора |

## Как читать схему

- **Чёрный овал** — СТАРТ / ФИНИШ.
- **Жёлтый ромб** — магистральный вопрос. «Нет» ведёт **вниз по цепочке**, «да» — **вбок**, в свою подветку.
- **Оранжевый ромб** — уточняющий вопрос внутри ветки.
- **Цветной прямоугольник** — ответ: дистрибутивы + короткий стереотип.
- **Серая заливка** — мёртвые легенды.
- **Сплошная стрелка** — `if/else` (`да` / `нет` подписаны).
- **Пунктирная стрелка** — «или» (равноценная альтернатива).
- **Цветная рамка** — одна ветка, всё внутри связано локально.

Схема построена **цепочкой, а не звездой**, читается как **вертикальный плакат-лесенка сверху вниз**.

## Маршрут за 30 секунд

1. Играешь в AAA? → гейминг
2. ПК слабый (≤8 ГБ, 10+ лет)? → воскрешение железа
3. Сервер / NAS / homelab? → серверы + NAS + роутеры
4. Анонимность / пентест? → приватность
5. Монтаж / музыка / дизайн? → творчество
6. Кодишь? → разработка
7. Нужны 1С / Office / Photoshop? → офис
8. Apple + есть деньги? → macOS / Hackintosh / Asahi
9. «Просто работает» или «сам настрою»? → два больших дерева Linux
10. Экзотика / ретро / музей → BSD, illumos, Haiku, ReactOS, FreeDOS

## Как перерисовать после правок

```bash
dot -Tsvg flowchart.dot -o flowchart.svg
python3 wiki_raw/svg_label_backing.py
rsvg-convert -w 16000 flowchart.svg -o flowchart.png
rsvg-convert -f pdf flowchart.svg -o flowchart.pdf

dot -Tsvg flowchart_simple.dot -o flowchart_simple.svg
rsvg-convert -w 4000 flowchart_simple.svg -o flowchart_simple.png
rsvg-convert -f pdf flowchart_simple.svg -o flowchart_simple.pdf
```
