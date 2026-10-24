# Ugly Face 3 SMD: test procedure

Board: `UglyFace_03` (TL072 + TLC555, 5 knobs, 1590B). Refs and values are from the KiCad schematic (`UglyFace_03_schematic.pdf`).
Expected values are hand calculations at **+9V = 8.8 V** (a 9.1 V supply minus the SS14 drop). Scale them if your supply differs.
Where Ugly Face 1 taught us something, it's noted as **UF1:**.

## How UF3 differs from UF1

| | UF1 | UF3 |
|---|---|---|
| Fuzz/preamp | LM386, gain 200 | **TL072 (U1A) non-inverting, gain 1 + 200k/1k = 201**, biased at VB = V+/2 |
| Output | 555 only (DISCH → VOLUME) | **MIX (RV4)** blends dry preamp and 555, then **U1B gain 4.1** → VOLUME |
| Timing cap | 100n | **C10 470n** (about 5× lower pitch) |
| THRESHOLD divider | 22k / B10k / 1k | **56k** / B10k / 1k |
| Vactrol LED drive | direct | **R7 100 Ω** series |
| Power LED | 1k | **R19 2k** (~3.4 mA) |

## Scope and meter setup (lessons from UF1)

- **DC coupling** for everything here. AC coupling turns square waves into slopes.
- **Time/DIV clicked into a detent**, and the VAR knob at CAL. Between detents, the times are wrong.
- **Probe ×1/×10** on the probe must match the scope channel setting.
- Ground clip on a board GND pad (J2/J4/J6/J8).
- f = 1 / (divisions for one **full** cycle × Time/DIV).

---

## 0. Before power

| # | Check | Expected | Measured | OK |
|---|---|---|---|---|
| 0.1 | Visual: U1/U2 pin-1 dots, D1 band, C1/C8 polarity (electrolytics), D2 and vactrol orientation | as silkscreen | - | x |
| 0.2 | Ohms, red on J1 (9V), black on GND. **Wait for it to settle** (C1 is 100µ, so this takes longer than on UF1) | climbs, then tens of kΩ. **Fail: a few Ω** | 24K | x |
| 0.3 | Ohms, red on +9V (D1 cathode), black on GND | settles around 10–20k (VB divider 20k ∥ THRESHOLD divider 67k ∥ ICs) | 18K | x |
| 0.4 | Diode test, red on J1, black on D1 cathode | 0.15–0.3 V | 0.227V | x |

## 1. First power (100 Ω in series with the 9 V; knobs at noon; no input)

**Fit all five pots first.** Without them, several nodes float and the readings mean little:
- **RV2 missing:** RESET (U2 pin 4) floats (CMOS input).
- **RV3 missing:** no timing resistor.
- **RV4 missing:** U1B's + input has no DC path to VB, so the mix output drifts to a rail.

(Section 0 was done without pots: 0.3 settled at 18k = the VB divider 20k ∥ ICs, as expected with the THRESHOLD divider open. With the pots fitted, expect ~15k.)

Every 0.1 V across the 100 Ω means 1 mA.

| # | Check | Expected | Measured (V across 100 Ω) | mA | OK |
|---|---|---|---|---|---|
| 1.1 | LED off (J7 open) | **~3.7 mA** (TL072 ≈ 2.8 + VB divider 0.44 + THRESHOLD 0.13 + 555 0.2) | 0.43V | 4.3 mA | x |
| 1.2 | LED on (J7 to GND) | **~7 mA** (+3.4 mA LED) | 0.73v | 7.3 mA (LED +3.0) | x |
| 1.3 | THRESHOLD full up (555 running), FREQUENCY at max pitch | rises ~1–2 mA (the 555 charging 470n) | 0.8v | 8.0 mA (555 +0.7) | x |

Unplug if anything reads above 2 V (20 mA). **Remove the 100 Ω before section 2.**

## 2. DC voltages (no input; black probe on GND)

| # | Node | Where | Expected | Measured |
|---|---|---|---|---|
| 2.1 | +9V | D1 cathode / U1 pin 8 / U2 pin 8 | supply − 0.2–0.3 V | 8.83v |
| 2.2 | LED anode (LED on) | D2 + | ~2 V; current (8.8 − V) / 2k ≈ 3.4 mA | 1.9v |
| 2.3 | **VB** (bias) | C4 + / RV4 wiper (MIX middle pin) | **4.4 V** (V+/2) | 4.4v |
| 2.4 | U1 pin 3 (U1A +) | - | 4.4 V (via R4 1M from VB) | 4.0v |
| 2.5 | **U1 pin 1 (PRE_OUT)** | - | **4.4 V** (DC gain 1, thanks to C7) | 4.4v |
| 2.6 | U1 pin 2 (U1A −) | - | 4.4 V | 4.4v |
| 2.7 | U1 pin 5 / pin 6 (U1B + / −) | - | 4.4 V / 4.4 V | 4.4v / 4.4v |
| 2.8 | **U1 pin 7 (mix out)** | - | **4.4 V** (DC gain 1, thanks to C15) | 4.4v |
| 2.9 | U2 pin 5 (CONT) | - | **5.87 V** (⅔ V+) | 5.9v |
| 2.10 | U2 pin 4 (RESET), THRESHOLD at the low end | - | **0.13 V** (8.8 × 1k / 67k) | 0.13v |
| 2.11 | U2 pin 4 (RESET), THRESHOLD at the high end | - | **1.44 V** (8.8 × 11k / 67k) | 1.9v|
| 2.12 | U2 pins 2/6 (TIMING), 555 running | - | ~4.4 V avg (scope: 2.93 ↔ 5.87 V) | 3.3v |
| 2.13 | U2 pin 3 (OSC_SQ): running / held in reset | - | ~4.4 V avg / 0 V | 4.0v |
| 2.14 | Vactrol LED anode (RV1 wiper) | - | 0 V | 0v |
| 2.15 | OUT pad (J5) | | 0 V (after C16) | 0v |

**If PRE_OUT or the mix output is far from 4.4 V**, check VB first (the R1/R2 divider and C4). Everything in U1 sits on VB.

## 3. Gate: THRESHOLD and the reset threshold

**Prediction:** with the 56k top resistor, RESET only reaches 1.44 V. If this TLC555 trips at ~1.0 V like UF1's, the gate opens at 8.8 × (1k + x) / 67k = 1.0, so x ≈ 6.6k, about **two-thirds of the way round**. Above that it drones; below it, it's gated.

1. No input. Scope on U2 pin 3.
2. Turn THRESHOLD up slowly from the low end until the 555 **just starts**.
3. Read U2 pin 4 (the reset threshold) and note the knob position.

| # | | Measured |
|---|---|---|
| 3.1 | Reset threshold (V) | 1.53V |
| 3.2 | Knob position where it opens (o'clock or %) | Starts at about 75%. Does not stop until the knob is turned down to about 25% |
| 3.3 | Does THRESHOLD feel like 3 settings (gated / glitchy / on), like UF1? | Maybe |

## 4. Oscillator (THRESHOLD up so it drones; MIX fully to the oscillator side; no input)

**Predictions:**
- Ideal: f ≈ 0.72 / (R × 470n), from **~15 Hz** (R = 100.5k) to **~3.3 kHz** (R = 470 Ω).
- **UF1:** the TLC555's output resistance (~400 Ω) added to R10 and pulled the top down. With R10 + ~400 Ω, expect a top of about **1.8 kHz**, with sag on the square.
- **New in UF3:** the oscillator is taken from **DISCH** (only pulls down; 100k R11 pull-up), and it now drives **R13 15k** into the mix (~15–25k load). At the **high-pitch** end the pull-up is weak, so the DISCH high level should drop to roughly **⅓ of 8.8 V**. At the **low-pitch** end the FREQUENCY wiper ties DISCH to pin 3, so it reaches nearly full swing.
  - **Prediction: the oscillator gets quieter as the pitch goes up** (up to ~10 dB).

| # | Check | Expected | Measured |
|---|---|---|---|
| 4.1 | U2 pin 3, FREQUENCY at the low-pitch end: period and frequency | ~15–25 Hz (UF1 ran faster than predicted at this end) | 30mS |
| 4.2 | U2 pin 3, FREQUENCY at the high-pitch end | ~1.8 kHz, square with sag | 0.2mS |
| 4.3 | Ohms, power off, U2 pin 3 → pin 2, FREQUENCY at the low-pitch end | ~100.5k | 93K (started at 90 and slowly climbed up to 93, why?) |
| 4.4 | **U2 pin 7 (DISCH) high level, low-pitch end** | ~8.5 V | 4.3V with Threshold up. With Threshold down its 0V|
| 4.5 | **U2 pin 7 (DISCH) high level, high-pitch end** | ~3 V (loaded) | 0V Measured with multimeter |
| 4.6 | U1 pin 7 (mix out), MIX full oscillator, low-pitch end | square ~5–6 Vpp around 4.4 V (may just clip) | I see a perfect square wave at U2 pin 3. At the OUT I see sort of a spike about +4V to -3.5V? |
| 4.7 | Covering the vactrol changes the low-end pitch? | no (if it's light-tight) | I’m using an LED/LDR package in a plastic box. |

## 5. Signal path (guitar or a ~100 mVpp 200 Hz sine into IN)

| # | Point | Expected | Seen |
|---|---|---|---|
| 5.1 | U1 pin 1 (PRE_OUT) | **gain 201:** 100 mVpp → would be 20 Vpp, so **hard-clipped square ~6–7 Vpp around 4.4 V**. Note the symmetry | |
| 5.2 | U1 pin 1 with a very small input (~10 mVpp) | ~2 Vpp clean sine. A check of the gain: 1 + 200k / 1k = 201 | |
| 5.3 | U2 pin 4 (RESET) | the preamp square, AC-coupled by C9, riding on the THRESHOLD bias | |
| 5.4 | U2 pin 3 | 555 bursts gated per guitar cycle, restarting each time (sync) | |
| 5.5 | Vactrol LED anode, ENVELOPE max | positive half-cycles, clamped at ~1.8–2 V by the LED | |
| 5.6 | Pitch vs playing level (ENVELOPE up) | louder → higher, with a slow swoop | |
| 5.7 | U1 pin 7, **MIX full dry** | the clipped preamp square × ~0.7 (the mix network ≈ ⅙, then U1B × 4.1) ≈ 4 Vpp | |
| 5.8 | U1 pin 7, **MIX at noon** | dry and oscillator summed | |
| 5.9 | OUT (J5), VOLUME max | same as U1 pin 7, centred on 0 V (after C16) | |

**Vactrol LED current (new R7 100 Ω):** with the 100 Ω supply resistor back in, compare the supply current at ENVELOPE 0 vs max with a strong signal. R7 should keep the extra to a few mA.

## 6. Audio probe trace (low volume)

IN → U1 pin 3 (clean) → U1 pin 1 (loud fuzz) → U2 pin 4 (gated fuzz) → U2 pin 3 (synth tone) → U2 pin 7 → U1 pin 7 (mix) → OUT.

## Notes / surprises

- **Section 1 (2026-10-02):** 4.3 mA idle, LED +3.0 mA, 555 at max pitch +0.7 mA. All as predicted (100 Ω method: move the decimal two places).
- **2.4 U1 pin 3 = 4.0 V vs 4.4 V: meter loading.** The pin is fed through R4 1M; a 10 MΩ meter makes a divider, 4.4 × 10 / 11 = 4.0 V. The circuit is fine.
- **2.2 LED anode 1.9 V:** a red, yellow or green LED; (8.83 − 1.9) / 2k ≈ 3.5 mA.
- **2.10/2.11 RESET 0.13–1.9 V (predicted 0.13–1.44 V).**
  - First guess (RV2 ≈ 14k) was **wrong**. Powered divider check: V(R9) = 131 mV, so I = 0.131 mA; V(pot) = 1.32 V, so **RV2 = 10.1k**; V(R8) = 7.35 V, so **R8 = 56.1k**. Sum 8.80 V ✓. The ohms reading (8.9k in circuit) agrees.
  - So the divider can only reach 1.45 V. **1.9 V means ~50 µA is flowing into the RESET node from somewhere else** (0.45 V across the node's ~9.3k Thevenin resistance).
  - **Suspect: leakage from U2 pin 3 (OUTPUT, next to pin 4):** flux residue or a partial bridge, ~50–150k.
    - This fits the low end reading normal: the 555 is in reset there, so pin 3 sits at 0 V and pushes no current.
  - **C9 leakage from PRE_OUT (4.4 V) doesn't fit:** it would also lift the low end to ~0.2 V.
  - If confirmed, it acts as positive feedback (once the 555 runs, its output holds RESET up), making the gate "sticky".
  - Tests:
    1. THRESHOLD fully up: measure pot lug 3. **1.9 V (not 1.45 V) confirms injected current.**
    2. Inspect U2 pins 3/4 under magnification; clean with isopropyl alcohol; re-measure.
- **Section 3 (2026-10-02): THRESHOLD has hysteresis. The oscillator feeds back into its own gate.**
  - FREQUENCY low: on at ~75% (divider ≈ 1.1 V, the reset threshold), off at ~25–30%. FREQUENCY ~75%: on/off ~10% apart. FREQUENCY max: on 75%, off 65%. **Strongest at low pitch.**
  - Grounding IN (jumper IN–IG) barely changed it, so the pickup is not via the input pad.
  - Scope, FREQUENCY low, oscillator running, no input:
    - U1 pin 1 (PRE_OUT) ~4.4 Vpp square.
    - **U1 pin 3 (+in) ~50 mV** (× 201 ≈ 10 V, so it clips).
    - **VB ~120 mV and +9V ~120 mV ripple.**
    - U2 pin 4 dips to **≈ −0.75 V** (the internal protection diode is conducting: the CMOS stress from `Build Notes.md`).
  - **Loop:** 555 → supply ripple → VB → R4 1M → U1A + input (× 201) → PRE_OUT square → C9 → RESET. The pin-4 diode clamps the negative half, pumping C9 so RESET's average rises and holds the 555 on.
    - Possibly a second loop: PRE_OUT driving the vactrol LED (R7/C8) and C9 pulls current from +9V, adding more ripple.
  - **Open questions:**
    - VB ripple equals the +9V ripple, but C4 22µ should cut it ~10× at low frequency. Either C4 isn't filtering, or the ripple is ground bounce between the scope clip and the probed area.
    - Was the 100 Ω still in series (it would raise the ripple a lot)?
  - **Bench fixes to try:**
    1. Tack 100µ across C4 (+ to VB).
    2. Repeat with ENVELOPE at 0 (removes the vactrol load).
  - **v2 ideas:**
    - Bigger VB cap / an RC filter feeding the bias divider.
    - Raise the preamp LF corner (C7 10µ → 1–2.2µ, ~70–160 Hz) so slow ripple isn't amplified 201×.
    - RC-filter the 555's supply.
    - Series resistor into RESET.
- **Fix confirmed (2026-10-02):** with 100µ tacked across C4, THRESHOLD turns on *and* off at ~70% (divider ≈ 1.05 V = the reset threshold). **The hysteresis is gone, so the VB path was the loop.** C4 (22µ X5R 1206) is too small, and X5R loses a good part of its capacitance at 4.4 V DC bias. Follow-up done: RESET = **1.48 V** at THRESHOLD max (divider predicts 1.45 V, so the extra 0.45 V was the pumping loop, not a leak), and **reset threshold = 1.0 V** (same as UF1's TLC555).
- **Section 4 (2026-10-02):**
  - **Range: 30 ms → 33 Hz (low end), 0.2 ms → 5 kHz (high end).** Both are ~2× the prediction (16.5 Hz with the measured 93k, 3.3 kHz ideal).
    - **Both ends imply C10 is acting like ≈ 235 nF**, half of 470n. Low end: 0.72 / (33 Hz × 93k) = 235n. High end: 0.72 / 5 kHz = 144 µs ÷ 235n = 615 Ω, i.e. R10 470 + ~150 Ω TLC555 output.
    - Likely cause: **ceramic DC-bias derating** (C10 = C13967, 470n 0805 X7R, biased at 2.9–5.9 V), the same effect as C4. UF1's fast low end (C6 100n) is probably the same.
    - Check: C10 in capacitance mode, power off. The meter tests at a tiny voltage, so a reading near 470n confirms it by elimination.
  - **4.3 = 93k, climbing from 90k:** the meter's current is charging C10 through the pot, so the reading creeps up to the true value. 93k = RV3 −7%, within tolerance.
  - **4.4/4.5 were taken with a multimeter (average, not the high level).** Re-do on the scope. 4.5 = 0 V at the high-pitch end: was THRESHOLD up?
  - **4.6: OUT shows spikes (+4 / −3.5 V), not a square.** C12 100n into the mix's R13 15k is a ~100 Hz high-pass, so a 33 Hz square is *differentiated* into spikes. At low FREQUENCY settings the oscillator is mostly clicks.
    - Bench test: tack 1µ across C12.
    - C13 (dry path, same 100n/15k) also cuts the guitar below ~100 Hz.
- **C12 test:** 2.2µ across C12 made little difference to the OUT spikes, so the oscillator's coupling isn't the (only) cause. Next suspect: the **dry path**. If the preamp still picks up the oscillator, C13 (100n/15k) would differentiate PRE_OUT's square into spikes. To do: scope OUT with MIX full dry vs full oscillator, and PRE_OUT. C10 can't be measured with the user's meter. **Paused 2026-10-02 until the board is boxed with jacks; then listen and re-test.**
- **2.12/2.13 TIMING 3.3 V, OSC_SQ 4.0 V averages:** a DMM can't average a 15–50 Hz waveform reliably. Re-check on the scope in section 4.
