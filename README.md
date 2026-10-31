# assets
## Inhalt
- `img/JJJJ-MM/` – eigene Bilder für Posts (öffentliche raw-URLs für das Notion-Feld „Bild“)
- `tools/fd_popart.py` – FD-Comic-/Pop-Art-Stil für Porträts:
  `python3 tools/fd_popart.py <prefix> foto1.png [foto2.png foto3.png]`
  → `<prefix>_band.png` (1080x720, Bild-Feld) und `<prefix>_cut_N.png` (Freisteller für Stories/Videos).
  Benötigt: Pillow, numpy, scipy. Beste Ergebnisse mit einfarbigem Hintergrund.
