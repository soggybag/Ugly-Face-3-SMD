# Ugly Face 3 SMD: build notes and v2 ideas

## v1.1 changes (2026-10-03)

Bench fixes from v1.0, plus a clean dry path so MIX blends **clean guitar** with the synth square.

| Change | Parts | Why |
|---|---|---|
| Bias cap 22 µ X5R → **100 µ electrolytic** | C4 (C970685, same as C1/C8) | Confirmed fix for THRESHOLD hysteresis (ripple on VB reached the gain-201 preamp) |
| **22k in series with RESET** | R22 | CMOS protection: pin 4 no longer clamps tens of mA below GND every cycle |
| Preamp LF corner 16 → ~72 Hz | C7 10 µ → 2.2 µ (C377773) | Slow ripple isn't amplified ×201. Control path only; the dry signal isn't affected |
| **RC-filtered 555 supply** (V555) | R23 47 Ω, C18 22 µ, C3 moved onto V555 | Keeps the 555's current pulses off +9V and VB |
| Mix coupling 100 n → **1 µ** | C12, C13 (C28323) | Was a ~100 Hz high-pass that spiked low-pitch squares and thinned the guitar |
| **Clean dry stage** | U4A (TL072), R24 33k, R25 10k, C17 4.7 µ | Gain 4.3, never clips on normal pickups. U1A (gain 201) now drives only the gate and vactrol, unchanged |
| Optional dry soft clip | D3/D4, **not fitted**: compact 2.54 mm through-hole pads | Fit two 3 mm LEDs (red ≈ ±1.8 V) or standing 1N4148s (≈ ±0.6 V, more clipping). Square pad = cathode. The pads are in the bottom-middle, clear of every back-mounted pot, so the leads don't touch a pot housing |
| **Buffered VB** | U4B | MIX pot wiper and preamp bias return to a stiff 4.5 V |
| Mix balance | R13 15k → 47k | The 8 Vpp square was clipping U1B at the synth end; the clean dry is lower |
| **THRESHOLD → toggle** (as UF1 v1.2) | SW1 Taiway 100 ON-OFF-ON, R20 1k (GATED), R21 2k2 (ON), RV2 → 3362P 10k trimmer | The pot behaved like a 3-position switch anyway |

**Setting GLITCH:** toggle to centre, no input, turn RV2 until the 555 just starts (pin 4 ≈ 1.0 V), then back off slightly.

**Layout:** SW1 sits at the old THRESHOLD shaft (back side). R4/R5/R6 moved off its pins. RV2 3362P is bottom-left (front, adjust with the lid off). U4 and the dry-stage parts (R24, R25, C17, C19, D3/D4) are in the bottom-middle, close to U1 so the high-impedance input trace stays short. R19 (LED resistor) moved to the top band. R23/C18 are under U2. Re-routed with `_tools/autoroute.py` (20 vias, DRC 0/0, parity 0).

**Layout rule learned:** through-hole parts can't go under the back-mounted 16 mm pots. Each pot's body and terminal housing covers the board from the shaft down to its pin row, which is the whole top half on this board. The v1.0 9V/GND wire pads and two vactrol pins already sit under the FREQUENCY pot; trim those leads flush. The v1.0 board/schematic are in `autoroute-backups/UglyFace_03-v1.0.*`.

**Still open for later:** C10 timing cap (film/C0G, retune FREQUENCY), weak envelope (LDR / LED drive), the OUT spike investigation (re-test once boxed).


Findings from bench testing (see `Test Procedure.md`). UF1 findings that also apply here are in `../../Ugly Face 1 SMD/docs/Build Notes.md`, e.g. THRESHOLD acting like a 3-position switch.

## Protecting the CMOS 555 (2026-10-02)

The user has had 7555s die occasionally in past builds. CMOS inputs are damaged by being pulled **outside the supply rails** (below GND or above V+). Each pin has internal protection diodes to the rails. When one conducts, current is injected into the chip's substrate, which can trigger **latch-up**: a parasitic short across the supply that burns the chip unless the current is limited. Limits: inputs from −0.3 V to V+ + 0.3 V; supply ≤ 18 V (TLC555 / ICM7555).

**Where this board can do that (most likely first):**

1. **RESET (pin 4) is driven below ground on every guitar cycle.**
   - The preamp (U1A) output swings about ±3.5 V around its bias and is AC-coupled (C9 2.2µ) onto a RESET bias of only 0.13–1.44 V. The negative half pushes pin 4 down to about −3 V.
   - The pin's internal diode to GND clamps it at about −0.6 V. The current is limited only by the fuzz stage's output (tens of mA). That's substrate injection every cycle.
   - **Worst at power-down / unplugging:** the coupling cap still holds its charge while the fuzz output falls to 0 V, driving pin 4 several volts negative.
   - The clamp also *rectifies*: C4/C9 charge until the negative peaks sit at −0.6 V, which shifts the effective gate bias. That's part of how THRESHOLD actually behaves.
2. **UF1 only: DISCH (pin 7) drives the output jack** through C7 100n and VOLUME, with no buffer. A static zap or plugging transient on the OUT jack goes straight to the 555 pin. (UF3 is safe here: U1B buffers the output and R18 100 Ω isolates it.)
3. **Power-down:** C10/C6 (timing) and the other caps on 555 pins discharge back into the pins as V+ collapses. This is small energy, normally fine.
4. **Supply over-voltage:** SS14 protects against reverse polarity only. A 12–18 V adapter is within the 555's 18 V limit, but **UF1's LM386 is only rated to 15 V** (the TL072 on UF3 is fine).

**Precautions for the next revision:**

- **Series resistor into RESET: 10k–47k between the bias/coupling node and pin 4.**
  - RESET draws only pA, so the bias and the sound don't change.
  - The clamp current drops from tens of mA to < 0.5 mA.
  - This is the single most useful fix. One 0805 resistor.
- **Optional Schottky clamp** (BAT54S, one diode to GND and one to V+) on the node *before* that resistor, so the external diode takes the current instead of the chip.
  - Note: clamping is already happening inside the chip, so this keeps today's sound (the same −0.3 to −0.6 V DC-restore). It just moves the stress outside.
- **UF1: don't drive the jack from the 555 directly.** Add ~1k in series at minimum, or buffer it as UF3 does.
- **Optional over-voltage TVS** across the supply after D1 (e.g. SMAJ15A, or a 15 V zener with the SS14 acting as the series element), mainly for UF1's LM386.
- **Prefer the TLC555 (TI LinCMOS)** over generic ICM7555 clones; keep the 100n at pin 8 close to the chip (already done).
- Both boards already have the C11 10n on CONT, decoupling at pin 8, and series reverse-polarity protection.

## Next revision needed: oscillator → preamp feedback (bench test 2026-10-02)

- THRESHOLD has strong hysteresis at low pitch (on ~75%, off ~25%). The 555's supply ripple (~120 mV on +9V and VB, with the 100 Ω removed) reaches the gain-201 preamp through VB / R4. The amplified square goes through C9 to RESET, where the pin's internal diode clamps it (pin 4 measured at ≈ −0.75 V) and pumps RESET up. Details in `Test Procedure.md` (section 3 notes).
- **Confirmed fix (bench):** 100µ across C4 removes the hysteresis (on/off both at ~70%). **Mod for test units:** tack a 100µ electrolytic across C4 (+ to VB, the RV4 wiper side).
- **Fix list for the next PCB:**
  - **C4 → 100µ electrolytic** (or 47µ + an RC-filtered bias supply) instead of 22µ X5R 1206.
  - Raise the preamp low-frequency corner (C7 10µ → ~2.2µ).
  - Separate RC-filtered supply for the 555.
  - **10k–47k in series with pin 4** (CMOS protection).
  - Re-check ground routing around the preamp gain leg (R6/C7) vs the 555.
  - **C12 (oscillator → mix) 100n → 1µ:** the 100n/15k high-pass (~100 Hz) turns low-pitch squares into spikes. Consider **C13 (dry → mix) 100n → 470n–1µ** too (it currently cuts the guitar below ~100 Hz).
  - **Timing cap C10:** measured behaviour says 470n 0805 X7R acts like ~235n under bias (pitch range 33 Hz–5 kHz, not 15 Hz–3.3 kHz). Use a film (PPS/PET SMD) or C0G cap for stable pitch, or choose the value from the measurement. Same for UF1's C6.
- **Risk to the 555:** low with the TLC555 driven from a TL072 (its output current is limited to tens of mA), but pin 4 *is* outside the −0.3 V absolute maximum on every cycle. That happens with a guitar too, since it's how the gate works. The greater risks are power-down and hot-plugging, and LM386-driven gates (UF1), which can push far more current into the clamp. The boards are OK to hand out as test units; ask testers to report any dead 555 and how THRESHOLD feels.

## First audio test (2026-10-02): working

- **It works with a guitar.**
- **The FREQUENCY low end is too low.** Measured 33 Hz at the bottom (section 4), which is sub-bass and mostly unusable.
  - Fix: smaller timing cap, or a larger minimum resistance on the pot.
  - Retune together with the C10 derating issue (a 470n 0805 X7R acts like ~235n). Pick a stable cap (film/C0G) and choose the range from the measurement.
  - The roadmap already suggests R10 470 → 1k2 to trim the top.
- **The envelope (pitch bend from playing level) is weak.**
  - Likely the LDR choice: its lit resistance isn't low enough compared with the 0–100k FREQUENCY resistance it sits across, and/or the LED isn't driven hard enough (R7 100 Ω + ENVELOPE B1k, and the vactrol LED only conducts on positive peaks).
  - To try: a lower-resistance/faster LDR; check how bright the vactrol LED gets (scope its anode at ENVELOPE max); reduce R7.
  - Longer term, the roadmap's idea of replacing the LDR with a transistor/op-amp control would make this repeatable.
