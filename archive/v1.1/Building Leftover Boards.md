# Building a leftover v1.1 board

Bench-tested 2026-10-15 (`docs/Test Procedure v1.1.md`). The v1.1 boards work. Build them as the BOM says, with the changes below.

## 1. Changes to make while building

| Part | Board value | Fit instead | Status | Why |
|---|---|---|---|---|
| **R21** (ON bias) | 2k2 | **15k** (0805) | **Tested, keep** | With 2k2, ON is a pure drone: the bias (6.7 V) sits so high that the guitar can't pull RESET below the ~1 V threshold. With 15k, ON drones when you're quiet and notes cut in. Rule: **the guitar must affect the sound in every THR position** |
| **R13** (oscillator → MIX) | 47k | **220k** (try 330k) | Not tested yet | The oscillator is ~17 dB louder than the dry signal, so MIX only goes ~25 % before the synth swamps the guitar. 220k should put unity near noon |
| Vactrol LED | (no series R) | — | Leave stock | R7 100 Ω is already in series. UF1 needed the extra resistor; UF3 doesn't |

## 2. ENVELOPE (RV1): keep the stock wiring

Leave **RV1 lug 1 to GND**, as the board has it. It only responds above ~50 % of the rotation, but it works. Everything tried so far was worse:

| Try (2026-10-15/16) | Result |
|---|---|
| Lug 1 lifted (series rheostat) | **No envelope.** C8 has no DC return, so it charges up and the LED stops conducting |
| Lug 1 lifted + 1N4148 lug 3 → GND (cathode on lug 3) | **Too strong:** slow decay, the LED is always slightly lit |
| Lug 1 lifted + 2k2 lug 3 → GND | **Too weak** |

Not tried yet (optional): the 1N4148 *with* ~1k in series (between the diode and the 2k2 results), or R7 100 Ω → 220–470 Ω with the diode. The real fix is a v1.2 change (see below).

## 3. Assembly notes

- **Through-hole leads under the back-mounted pots:** trim the 9V/GND wire-pad leads and the vactrol leads flush. They sit under the FREQUENCY pot body.
- **D3 / D4 (dry soft clip):** leave them empty. Optional: two 3 mm LEDs or standing 1N4148s (square pad = cathode).
- **SW1 THR:** lever **up = ON**, centre = GLITCH, down = GATED.
- **Set GLITCH (RV2 trimmer):** toggle to centre, no input, scope U2 pin 3. Turn RV2 until the 555 just starts (pin 4 ≈ 1.0 V), then back off a hair.
- **CMOS protection:** R22 22k on RESET is already on the board. The BAT43 / BAT54S clamp proven on UF1 is optional here: fit it if a 555 ever dies.

## 4. Expected readings (unit 1)

- Supply: 7.4 mA with the LED off, +2.6 mA with it on.
- DC: VB / PRE_OUT / DRY_OUT / mix out all **4.39 V**; CONT 5.84 V; reset threshold 1.05 V.
- Ripple: +9V ~4 mV; V555 ~50 mV "shark fin" (normal); PRE_OUT flat (~8 mV).
- FREQUENCY range: ~33 Hz – 5 kHz. The low end is sub-bass, because C10's 470n X7R behaves like ~235n under bias.

## 5. Still untested on v1.1

Section 4 (oscillator: low-end square shape and level vs pitch), GLITCH and GATED with a guitar, and the R13 change.
