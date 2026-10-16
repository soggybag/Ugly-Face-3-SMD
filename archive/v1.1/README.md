# Ugly Face 3 SMD v1.1: archived revision

- **Git tag:** `v1.1` (commit `6446f31`, 2026-10-06)
- **Tag note:** v1.1: ordered from JLCPCB (October 2026 batch)
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
- `production`/

`production/` holds the files sent to JLCPCB for this revision: UglyFace_03.zip, UglyFace_03_hand_solder.csv, bom.csv, designators.csv, netlist.ipc, positions.csv.

**Building a spare v1.1 board?** Read `Building Leftover Boards.md` first: R21 → 15k, R13 → 220k, and how to wire ENVELOPE.
