# Ugly Face 3 SMD v1.3: archived revision

- **Git tag:** `v1.3` (commit `5b2c955`, 2026-10-23)
- **Tag note:** v1.3 = FU-2: first JLC order of the new envelope board (C21 4.7u, R8 47k, silk FU-2 v1.3); fab files 2026-10-23
- **Archived:** 2026-10-23 with `_tools/archive_version.py`

## Finding a part

1. Open `UglyFace_03_ibom.html` in a browser. Type a reference (R14) or a value (100k) in the filter box; the part lights up on the board.
   - Hover over a pad to see its net.
   - F / B switch sides.
2. Find the same reference in `UglyFace_03_schematic.pdf` with Cmd-F.
3. `UglyFace_03_board_front.pdf` / `_back.pdf` are printable: page 1 has the outlines and references, page 2 the copper. The back is mirrored, as you see it holding the board.

## Files

- `UglyFace_03_board_back.pdf`
- `UglyFace_03_board_front.pdf`
- `UglyFace_03_ibom.html`
- `UglyFace_03_render_bottom.png`
- `UglyFace_03_render_top.png`
- `UglyFace_03_schematic.pdf`
- `docs`/
- `parts.csv`
- `production`/

`production/` holds the files sent to JLCPCB for this revision: UglyFace_03.zip, UglyFace_03_hand_solder.csv, bom.csv, designators.csv, netlist.ipc, positions.csv.
