# Ugly Face 3 SMD v1.1: test procedure

Board: `UglyFace_03` **v1.1** (git tag `v1.1`; `archive/v1.1/` has the schematic PDF and the interactive BOM). TL072 ×2 + TLC555, 1590B.
General method: `../../_tools/BENCH_TESTING.md`. The v1.0 results and the bench findings that drove v1.1 are in `Test Procedure.md`.

## What's new in v1.1 (what this procedure checks)

| v1.0 bench finding | v1.1 fix | Check |
|---|---|---|
| THRESHOLD had hysteresis: 555 ripple → VB → preamp ×201 → RESET (fixed on the bench with 100µ on C4) | **C4 100µ**, **VB buffered by U4B**, **C7 10µ → 2.2µ** (preamp gain falls below ~70 Hz), **R23 47 Ω + C18 22µ** filtering the 555's supply (V555) | Sections 2 and 3 |
| RESET driven below ground | **R22 22k into U2 pin 4** | Section 3 |
| OUT showed spikes, not a square, at low FREQUENCY (100n couplings) | **C12 and C13 → 1µ**, R13 15k → **47k** (less DISCH loading) | Section 4 |
| (new feature) | **Clean dry path**: U4A ×4.3 (R24 33k / R25 10k / C17 4.7µ) feeds the MIX dry side instead of the fuzz. D3/D4 pads (DNP) for optional soft clipping | Section 5 |
| THRESHOLD pot | **THR toggle** SW1 (ON-OFF-ON): RV2 3362P 10k trim = GLITCH; R21 2k2 to +9V = ON; R20 1k to GND = GATED | Section 3 |

## 0. Before power

| # | Check | Expected | Measured |
|---|---|---|---|
| 0.1 | Visual: U1, U2, U4 pin 1; D1 band; C1/C4/C8 polarity (100µ electrolytics); vactrol; SW1; RV2 | as silkscreen | ✅ |
| 0.2 | Ohms J1 → GND (slow: C1 and C4 are 100µ) | tens of kΩ; **fail: a few Ω** | 35.5K |

## 1. First power (100 Ω; knobs at noon; SW1 centre; no input)

| # | Check | Expected | Measured |
|---|---|---|---|
| 1.1 | LED off | **~6.5 mA** (two TL072s ~5.6 + dividers + 555). v1.0 was 4.3 mA with one TL072 | 0.74V -> 7.4mA |
| 1.2 | LED on | +~3.4 mA (R19 2k) | 1.03V -> 10mA |

## 2. DC voltages (no input)

| # | Node | Where | Expected | Measured |
|---|---|---|---|---|
| 2.1 | +9V | U1 pin 8 | supply − ~0.25 V | 8.8V |
| 2.2 | **V555** | U2 pin 8 | ≈ +9V (only ~10 mV lower through R23 47 Ω) | 8.79V |
| 2.3 | VB_RAW | U4 pin 5 / C4 + | 4.4 V | 4.39V |
| 2.4 | **VB** (buffered) | U4 pin 7 | 4.4 V | 4.39V |
| 2.5 | U1 pin 1 (PRE_OUT) | | 4.4 V | 4.39V |
| 2.6 | U4 pin 1 (DRY_OUT) | | 4.4 V | 4.39V |
| 2.7 | U1 pin 7 (mix out) | | 4.4 V | 4.39V |
| 2.8 | U2 pin 5 (CONT) | | ~5.9 V | 5.84V |

**Ripple check (scope, AC coupling, 10–20 mV/div), SW1 ON so the 555 runs, FREQUENCY low:**

| # | Point | v1.0 | v1.1 expected | Measured |
|---|---|---|---|---|
| 2.9 | +9V ripple | ~120 mV | smaller (the 555's current pulses now come from C18 22µ via R23) | I see a 50mV shark fin at C18 and R23, on the other other side of  R23 I see a smaller about 4mV wave. |
| 2.10 | V555 ripple | n/a | some (it's the 555's own local supply) | Not sure what you’re asking me to test here? |
| 2.11 | **VB ripple** | ~120 mV | **a few mV** (C4 100µ + U4B buffer) | I see nothing at C4 and U4 pin 7. I do see a 5mV triangle at U4 pin 8. |
| 2.12 | U1 pin 1 (PRE_OUT), no input | ~4.4 Vpp square (the feedback loop) | **flat** | I see about 8mV noise overlaid on a triangle at U1 Pin 1.  |

**Sections 0–2 notes (2026-10-15): all pass; the v1.1 supply fixes work.**
- **0.2** 35.5 kΩ ✓.
- **Supply current:** LED off 7.4 mA (estimate ~6.5 ✓); the LED adds 2.6 mA ✓.
- **DC:** every node is spot on.
  - +9V 8.8 V; V555 8.79 V (R23 drops ~10 mV); VB_RAW / VB / PRE_OUT / DRY_OUT / mix out all 4.39 V.
  - CONT 5.84 V = ⅔ of V555 ✓.
- **Ripple, reading your measurements:**
  - **2.9 +9V ripple ≈ 4 mV** (the far side of R23). v1.0 had ~120 mV, so it's **~30× better**.
  - **2.10 V555 ripple ≈ 50 mV** "shark fin" (C18 / R23 on the 555 side). That's what 2.10 asked: V555 is the 555's own little supply (U2 pin 8 = C18 +). The 555's current pulses now stay there, behind R23, instead of riding on +9V. Expected and harmless.
  - **2.11 VB: nothing visible** at C4 and U4 pin 7 ✓.
    - The 5 mV triangle at U4 **pin 8** is U4's **supply pin** (+9V), so it's the same ~4 mV +9V ripple as 2.9, not VB.
  - **2.12 PRE_OUT: ~8 mV of noise on a small triangle**, instead of v1.0's 4.4 Vpp square ✓.
    - Through the ×201 preamp that's only ~40 µV at its input: the feedback loop that caused the THRESHOLD hysteresis is gone.
    - If the triangle follows the FREQUENCY knob, it's residual 555 coupling. At 8 mV it's harmless next to a guitar signal.

## 3. THR toggle and the gate

GATE_BIAS is the RV2 wiper. U2 pin 4 reads the same (R22 carries no DC current).

| Position | Adds | Pin 4 (predicted at 8.8 V) |
|---|---|---|
| GLITCH (centre) | RV2 alone: R8 56k / RV2 10k / R9 1k → range **0.13–1.44 V** | set to the reset threshold (**~1.0 V** on v1.0's chip) |
| ON | R21 2k2 to +9V | **~6.9 V** |
| GATED | R20 1k to GND | **~0.13 V** |

1. SW1 centre, no input, scope on U2 pin 3. Turn RV2 until the 555 just starts; read pin 4 (the reset threshold). Back off a hair for the glitch edge.
2. **Hysteresis check (the v1.0 bug):** turn RV2 slowly up until it starts, then down until it stops. On v1.0 these were 50 % of the rotation apart. **v1.1: the same point** (within a few %).
3. Flip SW1 both ways; read pin 4; label which lever direction is ON and which is GATED.

| # | Check | Measured |
|---|---|---|
| 3.1 | Reset threshold (V) | 1.05V |
| 3.2 | Start / stop points of RV2 (hysteresis) | Not sure what you’re asking? |
| 3.3 | Pin 4: GLITCH / ON / GATED | 1.04V |
| 3.4 | Lever direction for ON | Up |

## 4. Oscillator (SW1 ON; MIX fully to the oscillator side; no input)

| # | Check | Expected (v1.0 measured) | Measured |
|---|---|---|---|
| 4.1 | U2 pin 3, FREQUENCY low end | ~33 Hz (C10 acts ~235n from DC-bias derating) | |
| 4.2 | U2 pin 3, FREQUENCY high end | ~5 kHz | |
| 4.3 | **OUT at the low FREQUENCY end** | **a square** (v1.0: spikes). C12 1µ into R13 47k passes down to ~3 Hz | |
| 4.4 | Oscillator level, low vs high FREQUENCY | v1.0 predicted it gets quieter as pitch rises (DISCH loading); R13 47k should reduce that | |

## 5. Signal path (guitar, or a 100 mVpp 200 Hz sine)

| # | Point | Expected | Seen |
|---|---|---|---|
| 5.1 | U1 pin 1 (PRE_OUT) | hard-clipped square, ~6–7 Vpp around 4.4 V (gain 201) | Hard clipped square waves seen. |
| 5.2 | **U4 pin 1 (DRY_OUT)** | **clean** copy of the input × 4.3 (100 mVpp → ~430 mVpp) | Looks like a clean signal |
| 5.3 | U2 pin 4 (RESET) | the preamp square, AC-coupled onto the THR bias | Looks like the preamp square |
| 5.4 | OUT, **MIX full dry** | **clean guitar** (new in v1.1; v1.0 gave the fuzz here) | Clean signal at the output. Is about unity at Volume 75%, a faint fuzz and be heard in the background.  |
| 5.5 | OUT, MIX full oscillator | gated, synced 555 bursts | Turning mix up to about 25% brings the output over unity. This is more fuzz than dry signal at this point. Would be good to get mid point of Mix to be about unity? |
| 5.6 | OUT, MIX noon | clean guitar under the synth | I can hear both, fuzz dominates mostly due to the square wave nature.  |
| 5.7 | ENVELOPE up | pitch rises with playing level | The envelope doesn’t have any effect until after 50% and you don’t really hear it until about 75%. |
| 5.8 | Low notes on the fuzz side | a little less bass than v1.0 (C7 2.2µ: ~70 Hz corner) |  |

NOTE! With the switch up the oscillator runs. In this mode The guitar has not effect. You only hear the oscillator. Seems like the guitar is NOT triggering the RESET. Turning up Envelope causes the guitar change the frequency but not because of a RESET, instead just the envelope is causing the frequency to change. You can hear the frequency changing but it is unrelated to notes played on the guitar.

When the threshold switch is up, oscillating, I see 6.72V on U2 pin 4. Seems like the guitar signal can’t bring this down below 1V to trigger a RESET? 

**Sections 3–5 notes (2026-10-15):**
- **The "guitar doesn't trigger RESET in ON" note: that's what ON does with these values (a design choice to revisit, not a fault).**
  - The preamp square reaches RESET through C9 2.2µ, swinging ~±3.3 V around the THR bias.
  - In **ON** the bias is 6.7 V, so the swing only reaches down to ~3.4 V, never below the ~1.0 V reset threshold. ON is a **pure drone**: the guitar can't reset it, and only ENVELOPE (through the vactrol) moves the pitch. That's exactly what you heard.
  - The **sync / glitch** sound is the **centre position (GLITCH)**: the bias sits at the threshold (1.04 V), and every cycle of the preamp square resets the 555.
  - **GATED** (bias ~0.13 V): silent until the positive half-cycles lift RESET above the threshold.
  - **To do:** check GLITCH and GATED with a guitar and record what each does (3.3 still needs ON / GATED pin-4 voltages).
  - **Option, if ON should interact:** R21 2k2 → **~15k** puts the ON bias at ~3.7 V. It drones when quiet, and hard notes swing below 1 V and "cut holes" (the original UF idea). 10k ≈ 4.5 V is borderline. A one-resistor swap (0805).
- **3.2 hysteresis, explained:** in GLITCH, no input. Turn RV2 slowly **up** until the 555 starts (note the trimmer position), then slowly **down** until it stops. v1.0 needed a big swing back down (hysteresis from the supply ripple loop). On v1.1 the start and stop points should be almost the same.
- **5.4 a faint fuzz at MIX full dry:** a little bleed through the pot / layout, normal for a pan-style mix pot. Ignore unless it's audible in use.
- **5.5 MIX balance (the oscillator is much louder):**
  - The oscillator is taken from DISCH (~8 Vpp) through C12 / **R13 47k**; the dry path is ~0.4 Vpp through R12 15k.
  - At MIX noon (each side ~5k to VB) the oscillator arrives ~7× (~17 dB) louder.
  - **Fix: R13 47k → ~220k–330k.** That brings noon close to unity, and also loads DISCH less. Try 220k first.
- **5.7 ENVELOPE only works above ~50–75%:**
  - The pot is a **divider** (pin 1 to GND), so below about half the wiper voltage can't reach the LED's ~1.8 V forward voltage.
  - **Bench test:** lift RV1 lug 1 (GND), so the pot becomes a **series rheostat** (R7 100 Ω + wiper-to-pin-3) in the LED path. The LED then always gets some drive and the knob sets how much (same direction).
  - If you like it, v1.2 wires it that way.

**Bench results (2026-10-15):**
- **R21 2k2 → 15k: works.** ON now drones and the guitar still cuts in. **Design rule from this test: in every THR position the guitar must audibly affect the sound** (it's a guitar pedal). → v1.2: R21 = 15k.
- **RV1 lug 1 lifted → the envelope disappeared.** That's because C8 (100µ) then has no DC return except through the LED:
  - It charges up on the positive peaks (through the LED) and nothing discharges it, so after a few cycles the LED never conducts again.
  - **Fix: give C8's pot side a path back to GND.** Either:
    - a **1N4148 from RV1 pin 3 to GND, cathode (band) on pin 3** (preferred): the negative half-cycles recharge C8, so the LED gets the full swing (a little more drive, like a voltage doubler); or
    - a resistor from RV1 pin 3 to GND (1k–2k2): simpler, a little less drive.
  - Current limiting is already there: R7 100 Ω + the pot. At full ENVELOPE the peaks are limited by the TL072 itself (~20 mA); fine for short peaks into a 5 mm LED. A 220 Ω R7 would be gentler if the LED or the op-amp output looks stressed.

**Optional (D3/D4, DNP):** standing 1N4148s or 3 mm LEDs across U4A's feedback soft-clip the dry path. Try them after the stock test.

## 6. After boxing

- Supply current again (1.1).
- Repeat 3.2 (hysteresis) with the jacks wired. Long wires can add a new feedback path.

## Record

| Item | Result |
|---|---|
| Unit number | |
| Date | |
| Notes | |
