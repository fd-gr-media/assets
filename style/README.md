# FD Industrial-Stil (ab 11/2026)

- `fd-wall-dark-v1.png` (1080×1350): Hintergrund für alle dunklen Flächen (statt #0F1115).
  Basis: Pexels-Foto 5622897 (freie Lizenz), stark abgedunkelt und entsättigt,
  eigene abgerissene Plakatreste (Blau oben links, Papier unten links),
  FD-Stencil im Logo-Stil unten rechts (gedämpft, Lime-Balken).
- In HTML: `background:#0F1115 url('…/style/fd-wall-dark-v1.png') center/cover`
- Generator-Skripte: `gen_wall_*.py` (gen_wall_dark_v1.py erzeugt die Datei).

- `fd-lime-wheatpaste-v1.png` (1080×630): Hintergrund für Lime-Flächen (statt #C6F432),
  z. B. unterer Teil des punkte-foto-Covers. Lime-Plakat aufgekleistert: Papierstruktur,
  Knicke, Kleisterblasen, ohne abgerissene Ecken; FD-Stencil im Logo-Stil sehr schwach.
  In HTML: `background:#C6F432 url('…/style/fd-lime-wheatpaste-v1.png') center/cover`

## Freigegeben für Lime-Cover (punkte-foto), Stand 06.11.2026
- `fd-lime-fd-stencil-v1.png` (1080×630): Lime-Fläche mit sehr schwachem FD im Logo-Stil.
  `background:#C6F432 url('…/style/fd-lime-fd-stencil-v1.png') center/cover`
- `fd-wheatpaste-overlay-v1.png` (1080×1350): Plakat-Overlay über das GANZE Cover (Foto + Lime):
  zwei Ebenen ganz oben im Cover:
  1. `background:url(…overlay) ; mix-blend-mode:soft-light`
  2. `background:url(…overlay) ; mix-blend-mode:multiply; opacity:.18`
  (`fd-lime-wheatpaste-v1.png` ist damit für das Cover nicht mehr nötig.)

## Freigegeben für blaue Folien (zahl/text), Stand 06.11.2026
- `fd-blue-fd-stencil-v1.png` (1080×1350): Blau #2346F5 mit sehr schwachem FD im Logo-Stil (dunkel, Lime-Balken) unten rechts.
  `background:#2346F5 url('…/style/fd-blue-fd-stencil-v1.png') center/cover`
- Darüber dasselbe Plakat-Overlay wie beim Cover (`fd-wheatpaste-overlay-v1.png`, soft-light + multiply .18).
