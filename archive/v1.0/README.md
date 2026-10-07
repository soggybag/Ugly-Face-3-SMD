# Ugly Face 3 SMD v1.0: archived revision

- **Git tag:** `v1.0` (commit `8f744a6`, 2026-10-02)
- **Tag note:** v1.0: boards as received from JLCPCB (2026-10-01), with bench-test docs
- **Archived:** 2026-10-06 with `_tools/archive_version.py`

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

`production/` holds the files sent to JLCPCB for v1.0 (copied from `production/v1.0-old-do-not-upload`).
