# Ugly Face — roadmap, notes and to-do

Discussion 2026-09-29. Baseline: **Ugly Face 3 SMD** (`UglyFace_03`, 1590B, 5 knobs: ENVELOPE, THRESHOLD, FREQUENCY, MIX, VOLUME).

## How UF3 works (from the schematic)

- **Preamp** U1A: gain 1 + 200k/1k = **201**. The output (PRE_OUT) drives three things at once: the dry path (C13 → MIX), the gate (C9 → 555 RESET) and the vactrol LED (R7 100 → C8 100u → ENVELOPE B1k → LED).
- **Gate:** THRESHOLD (B10k between 56k to +9V and 1k to GND) sets a DC level of about 0.15–1.4 V on RESET, and C9 adds the audio on top. The TLC555 runs whenever RESET is above about 1 V, which is **on the positive peaks of every guitar cycle**, not with a smooth envelope. With THRESHOLD high enough, the DC alone clears the reset level and the 555 free-runs (drones) with no input.
- **Oscillator:** TLC555 wired output-to-capacitor: pin 3 → FREQ (C100k) + R10 470 → C10 470n. The LDR sits in parallel with that timing resistance, so playing louder lowers R and raises the pitch, with the LDR's slow, laggy sweep. The oscillator output is taken from DISCH (R11 100k pull-up, C12).
- **FREQ range:** f ≈ 0.72/(R·C) gives **~15 Hz** (pot at 100k) to **~3.3 kHz** (470 Ω).
- **Mix/output:** U1B sums the preamp and the oscillator (15k each) → gain 4.1 → VOLUME.

## Idea 1 — replace the LDR/vactrol with standard SMD parts

**Opinion: yes. Build an envelope follower that drives the pitch.** The LDR does two jobs: it converts level to resistance, and it adds its own lag (fast-ish attack, slow release). Both can be done electronically:

- **Envelope follower:** a rectifier with an attack/release RC (roughly 5 ms attack, 50–300 ms release, which is the LDR's character; the release could be a DECAY control). Diode/BAT54S or an op-amp precision rectifier.
- **Pitch control** options, in the order I'd try them:
  1. **Transistor current source** charging C10 in parallel with FREQ. This gives the widest, most LDR-like pitch swing (10×+).
  2. **555 CONT pin (pin 5)** driven by the envelope. Simplest, but only about 1–2 octaves of swing, and it shifts the duty cycle.
  3. **2N7002 MOSFET as a variable resistor** (basic part C8545). Cheap, but the non-linear onset needs tuning.
  4. **SMD optocoupler** (PC817-type phototransistor). Keeps the "opto" idea, but it has no natural lag (add it with the RC), and the phototransistor only conducts one way, so it needs a diode in the timing path.
- Bonus: the same envelope can also drive Idea 5 (dynamics) and a cleaner gate. See the UF4 architecture below.

## Idea 2 — frequency range

**Opinion: trim the top, and keep the LDR (or its replacement) from dragging the low end up.**

- The unused top end: R10 470 Ω gives a 3.3 kHz maximum. **R10 → 1k2 gives a ~1.3 kHz top** and spreads the knob over the useful range. This is a drop-in value change to try on a built UF3 first.
- The low end is already about 15 Hz at the bottom of the pot. But while you play, **the lit LDR in parallel sets the real low end**: pot 100k in parallel with a lit LDR of about 5k is about 4.8k, which is about 320 Hz. More lows while playing means a series resistor on the LDR (for example 10k), or less LED drive (ENVELOPE lower).
- **Your mental model is close, but it doesn't drop out; it changes character.** Because the gate opens once per guitar cycle, a 555 slower than your note never finishes a cycle before the gate closes. The output becomes a pulse at the *guitar's* pitch (a gated square fuzz that follows your note) instead of a separate tone. Below about 20 Hz with THRESHOLD up (free-running), it turns into rhythmic chopping. So lower is usable; it just stops sounding like a second pitch.
- Taper: FREQ is C100k (reverse log). Check whether the dead travel is at the CW end; if so, R10 alone should fix it.

## Idea 3 — harsh clipping in the dry signal (UF3 mix)

**Opinion: give the dry signal its own clean path, and let the control path clip.**

- Gain 201 clips almost every note to a square wave. That's good for the gate and the LED, but it's also what you hear as "dry".
- **Just lowering the gain** makes the gate and vactrol weaker. RESET needs about 1 V of swing and the vactrol LED needs about 2 V to light. Around a gain of 30–50, normal playing still gates, but quiet notes and the LED suffer, and loud notes still clip.
- **Clipping diodes/LEDs in U1A's feedback** (soft clip at about ±1.8 V with red LEDs): the dry signal gets more musical and the gate still works, but LED drive, and so the vactrol effect, drops a lot. It's a quick experiment on a built UF3 (diodes across R5), but not my first choice.
- **Best:** a **clean unity buffer for the dry signal**, plus a separate high-gain stage that only feeds the gate and envelope. It costs one more op-amp half (TL072 + TL072, or a TL074). The dry signal is then truly dry. Balance the levels at the mixer, because the 555 square is much louder than the clean guitar.
- Optional later: a DRY toggle (clean / soft-clipped).

## Idea 4 — Atari Punk Console merge

**Opinion: yes. It fits as a sub-tone / "stepped" option, and possibly a spin-off.**

- The APC is a 555 astable that triggers a second 555 as a **monostable**. When the monostable's pulse is longer than the astable's period, triggers get skipped, which divides the pitch down into stepped sub-harmonics (octave down, fifth, and so on). The second pot (pulse width) sets which step.
- In the UF: the gated UF oscillator becomes the APC's first 555; the second 555 is a monostable with a PULSE/STEP knob. It stays silent with no input, as now, unless THRESHOLD is up. Mix the two outputs, or switch between them.
- **Dual CMOS 555:** yes: **TLC556** (TI), ICM7556, LMC556 (SOIC-14). But **two TLC555s** is fine and probably better at JLC. UF already uses TLC555 (an extended part), and a second one adds no new extended line, whereas a TLC556 would replace it as a new one. (NE555 is basic, but bipolar: supply spikes, higher current, not recommended here.)
- Needs a sixth control. Could replace MIX in a spin-off, or go in a 125B.

## Idea 5 — merge with the Penfold dynamic fuzz

**Opinion: best idea of the five. It fixes the "always full volume" problem.**

- The Penfold SMD already has an envelope-controlled LM13700 VCA. Replace its Rat stage with the UF oscillator: square wave → VCA → output that follows your playing dynamics.
- **Cheaper alternatives to the LM13700** (worth a breadboard test):
  - **Switched envelope:** a CD4053 analog switch (basic part C6742) flipped by the 555 selects between the envelope voltage and VREF. The output is a square wave whose amplitude *is* the envelope. No VCA chip.
  - **Envelope-powered 555:** power the TLC555 from a buffered envelope voltage. A CMOS 555's RC frequency doesn't depend on supply voltage, so amplitude follows the envelope while pitch stays put, and below about 2 V it stops (a natural gate). Needs a bench test for clicks and startup.
- Controls: DECAY (release), SENS (trimmer or knob).

## Proposed architecture — "Ugly Face 4 (Dynamic)"

Combines ideas 1, 2, 3 and 5; idea 4 as an option.

```
IN ─► U1A clean buffer ─────────────────────────────► DRY ─┐
        └► U1B gain stage (clips, control only) ─► gate (RESET)                 │
                                                  └► envelope follower (attack/DECAY)
                                                        ├► 555 pitch (replaces LDR)
                                                        └► VCA / switched envelope
TLC555 (FREQ, R10 1k2) ──────────────► VCA ──────────────► WET ─┤
   └► (option) 2nd TLC555 monostable = APC sub-tone                 │
                                                  MIX ─► output stage ─► VOLUME ─► OUT
```

- Parts: 2× TL072 (or TL074 + TL072), 1–2× TLC555, CD4053 or LM13700, BAT54S/1N4148W. All SMD, and the vactrol goes away.
- Enclosure: likely more than 5 controls. A 125B with the Hyper Fuzz drilling (5 knobs) plus toggles, or 6 knobs in a new drilling.

## Road map

1. **Phase 0 — value tweaks on a built UF3** (no new board):
   - R10 470 → 1k2 to trim the top end.
   - Try a 10k series resistor on the LDR.
   - Try LED/diode soft clipping across R5.
2. **Phase 1 — breadboard experiments:**
   - Envelope follower + transistor/CONT pitch control vs the LDR (match the sweep and lag).
   - Clean dry buffer + separate control-gain stage.
   - Switched-envelope (CD4053) vs LM13700 VCA vs envelope-powered 555.
   - APC second 555 monostable.
3. **Phase 2 — Ugly Face 4 (Dynamic)** schematic → PCB → JLC. Ideas 1, 2, 3, 5.
4. **Phase 3 — APC:** add to UF4 as an option if it fits, otherwise a spin-off ("Ugly Punk").

## To-do

- [ ] Phase 0: order/fit 1k2 for R10 on a UF3; note where the useful FREQ travel now ends.
- [ ] Phase 0: test a 10k series resistor on the LDR (more lows while playing?).
- [ ] Phase 0: test 2× red LEDs (antiparallel) across R5; listen to the dry signal and check the gate/vactrol still respond.
- [ ] Measure the LDR's behaviour on a UF3 (resistance lit/dark, and roughly how fast it releases) so the replacement can copy it.
- [ ] Check JLC stock/basic status: TLC555IDR, TLC556, PC817 SMD, BAT54S, CD4053 (C6742 basic), TL074.
- [ ] Decide the UF4 control set and enclosure (125B Hyper Fuzz drilling + toggles?).
- [ ] THRESHOLD → 3-position switch (GATED / GLITCH / ON), with a trimmer setting the GLITCH bias at the 555's reset threshold. (UF1 bench test 2026-10-01: the TLC555 resets at 1.0 V, and the pot behaves like 3 settings, not a range.) Details in `Ugly Face 1 SMD/docs/Build Notes.md`. Applies to UF3's gate too if it's built the same way.
- [ ] Protect the CMOS 555: 10k–47k series resistor into RESET (pin 4 is driven ~3 V below GND every cycle via the gate coupling cap), optional BAT54S clamp; on UF1-style boards, never drive the output jack straight from DISCH; optional TVS for over-voltage. Details in both boards' `docs/Build Notes.md`.
- [ ] Decide whether the APC goes in UF4 or its own spin-off.
- [ ] Simulate/breadboard the envelope follower attack/release values.
- [ ] Draw the UF4 schematic once Phase 1 picks the VCA and pitch-control method.

## Open questions

- Is the dead FREQ travel at the CW (top) end? That confirms the R10 fix.
- Keep the LDR's slow-release "chirp", or make it adjustable (DECAY)?
- Should the dry path offer a soft-clip option, or always be clean?
- UF4: keep MIX, or replace it with a DYNAMICS amount?

- UF4 VCA option (2026-10-02): the Trem SMD's discrete transistor VCA (bench-proven) is a JLC-friendly alternative to the LM13700 / CD4053 switched envelope. See `Trem SMD/docs/VCA Building Block.md`.
