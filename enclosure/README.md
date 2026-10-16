# Enclosure

Hammond 1590B. Panel art and drilling template.

- Keep the Affinity source files here (`.afdesign`; stored with Git LFS).
- **Also commit a PDF or SVG export** of each one, so reviewers without Affinity can see it, and so changes are visible in history.

## Drill guide (v1.1, generated 2026-10-15)

- **`UglyFace3_1590B_drill.csv`:** face holes for the Tayda Box Tool.
- **`UglyFace3_1590B_drill_template.svg`:** a 1:1 printable template (outside view, labelled, with a 50 × 5 mm check box).
- **`UglyFace3_1590B_mill_marks.svg`:** for the Othermill.

### Face (side A), outside view

| Hole | X | Y | Ø mm | Part |
|---|---|---|---|---|
| MIX (top left) | −17.95 | 36.22 | 7.5 | RV4 Alpha 16 mm B10k |
| FREQUENCY (top centre) | −0.17 | 36.22 | 7.5 | RV3 Alpha 16 mm C100k |
| VOLUME (top right) | 17.61 | 36.22 | 7.5 | RV5 Alpha 16 mm A100k |
| ENVELOPE (bottom left) | −17.95 | 10.82 | 7.5 | RV1 Alpha 16 mm B1k |
| LED (bottom centre) | −0.17 | 8.79 | 3.2 | D2, 3 mm, no bezel |
| THRESHOLD toggle (bottom right) | 17.61 | 9.42 | 6.5 | SW1 Taiway 100 (1/4" bushing), ON-OFF-ON |
| Footswitch | 0 | −37.5 | 12.2 | 3PDT (same position as the Trem / Penfold 1590B) |

- **Origin and units:** the origin is the face centre; mm, +X right, +Y up, viewed from outside. The top is the jack end.
- **Board-to-face mapping:** the box centre is at board (148.5, 119.5). The controls face the panel, so the outside view is mirrored: **X = 148.5 − x_board**.
  - Pot shafts are 16 mm above the pot pins: **Y = 119.5 − (y_pins − 16)**.
  - LED and toggle (centre pin): **Y = 119.5 − y**.
  - The same method gave UF1's CSV, which has been built.
- The control centre line is at X −0.17, not 0 (from the board placement). The footswitch stays on the true centre; 0.17 mm isn't visible.
- **Not included:**
  - the side-wall jacks / DC (mark by hand after a test fit);
  - the GLITCH trimmer (RV2) and the D3/D4 LED-clipping pads, which are internal.
- Hole sizes are for raw aluminium. For powder coat, add Tayda's allowance (+0.2 to +0.4 mm).

### Mill marking file (Othermill)

- **Page:** 60 × 112 mm = the 1590B face (portrait), outside view, **top edge = the jack end**.
- **Contents:** one circle per hole at its finished diameter, plus a 1 mm circle at each centre. Stroke only.
- **Alignment:**
  - Page placement: the lower-left page corner = the lower-left face corner.
  - Geometry placement: the marks' bounding box starts **8.30 mm from the left edge and 12.40 mm from the bottom edge** (it spans x 8.30–51.36, y 12.40–95.97).
  - Zeroing on the face centre (X 30, Y 56) is the most reliable; measure your box, since the walls have draft.
- The 1590B is ~31 mm tall: check it fits under the spindle with the engraving bit.
