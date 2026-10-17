"""UF3 v1.3 envelope: tilt -> LM358 peak detector with gain (SENS) -> ENV hold cap -> LM358 + MMBT3904 current sink for the vactrol LED.
Op-amps: behavioural LM358 on 8.8 V (output 0.02-7.4 V, ~0.3 V/us, Vos settable). Prints LED current at rest and peak for test bursts."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ng import run
OPA = """.subckt lm358 p m o
Bpre a 0 V=max(-0.5, min(8.0, 1000*(V(p)-V(m))))
Ra a x 1k
Cx x 0 27n
Bo oi 0 V=max(0.02, min(7.4, V(x)))
Ro oi o 50
.ends
"""
def net(amp, f, sens, rel, vos=0.0, tau=0.8):
    k = max(sens, 1e-6)   # ENVELOPE wiper position as a fraction of RV1 (A10k divider)
    return f"""uf3 envelope v1.3
.model D1N4148 D(Is=2.52n Rs=0.568 N=1.752 Cjo=4p)
.model DLED D(Is=1e-19 N=1.9 Rs=5)
.model Q3904 NPN(Is=6.7f Bf=200 Vaf=74 Rb=10)
{OPA}
V9 v9 0 8.8
Evb vb 0 v9 0 0.4989
Bin dry 0 V=V(vb)+{amp}*sin(6.2832*{f}*time)*exp(-max(time-0.05,0)/{tau})*(time>0.05 ? 1 : 0)
C20 dry n1 33n
R37 n1 top 10k
RVa top tp {max(10e3*(1-k),1)}
RVb tp vb {max(10e3*k,1)}
VOS tpo tp {vos}
XU5A tpo fbm o1 lm358
D5 o1 dk D1N4148
R27 dk env 1k
C21 env 0 1u
R28 env fbm 470k
R29 fbm vb 22k
RREL env vb {rel}
XU5B env m2 o2 lm358
R33 o2 b 1k
Q1 c b e Q3904
R34 e 0 330
R31 m2 v9 100k
R32 m2 e 100k
R36 m2 v9 1Meg
VIL v9 la0 0
R35 la0 la 100
DL la c DLED
.ic v(env)=4.39 v(c)=7
"""
def sim(amp, f, sens, rel, vos=0.0, t=1.5):
    out = run(net(amp, f, sens, rel, vos).splitlines() + ['.end'],
              [f'tran 20u {t} 0 20u uic',
               'meas tran irest avg i(VIL) from=0.02 to=0.05',
               'meas tran ipk max i(VIL) from=0.05',
               f'meas tran ilate avg i(VIL) from={t-0.1} to={t}',
               'meas tran envpk max v(env) from=0.05'])
    v = {}
    for l in out:
        l = l.replace('stdout ', '', 1).strip()
        for k in ('irest', 'ipk', 'ilate', 'envpk'):
            if l.startswith(k):
                try: v[k] = float(l.split('=')[1].split()[0])
                except Exception: pass
    return v
if __name__ == '__main__':
    print("Rest (no input): ENV and LED current vs detector offset, ENVELOPE max")
    for vos in (0, 0.007, -0.007):
        out = run(net(0, 82, 1, 220e3, vos).splitlines() + ['.end'], ['tran 50u 0.3 0 50u uic', 'meas tran env avg v(env) from=0.2 to=0.3', 'meas tran i avg i(VIL) from=0.2 to=0.3'])
        print("  Vos %+.0f mV: " % (vos*1e3) + "  ".join(l.replace('stdout ','').split('at=')[0].strip() for l in out if l.replace('stdout ','').strip().startswith(('env','i '))))
    print("\nDecaying note at DRY_OUT (0.8 s decay), RELEASE 22k+220k:  peak LED mA / LED mA at 1.4 s")
    for amp in (0.05, 0.2, 1.0, 3.0):
        for f, s_ in ((82, 'low E'), (330, 'high E')):
            row = []
            for k, lab in ((1, 'ENV max'), (0.25, 'ENV ~noon'), (0.05, 'ENV low')):
                v = sim(amp, f, k, 242e3)
                row.append(f"{lab}: {v.get('ipk',0)*1e3:5.1f} / {v.get('ilate',0)*1e3:4.1f}")
            print(f"  {amp:4.2f} Vpk {s_:6s}  " + "   ".join(row))
