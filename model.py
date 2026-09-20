import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

pH0, pM0, s = 0.30, 0.60, 0.05
alpha, beta, gamma, pi = 0.30, 0.40, 0.10, 0.20
T = 40
pH = np.zeros(T+1); pM = np.zeros(T+1); qH = np.zeros(T+1); qM = np.zeros(T+1)
pH[0], pM[0], qH[0], qM[0] = pH0, pM0, pH0, pM0
for t in range(T):
    pH[t+1] = (1-alpha)*pH[t] + alpha*s
    pM[t+1] = (1-beta)*pM[t] + beta*pH[t]
    qH[t+1] = (1-gamma)*qH[t] + gamma*pH[t]
    qM[t+1] = (1-gamma)*qM[t] + gamma*pM[t]

# closed-form checks
a = pH0 - s
t = np.arange(T+1)
pH_cf = s + a*(1-alpha)**t
d = pM - pH
d_cf = (1-beta)**t*(pM0-pH0) + a*alpha*((1-beta)**t-(1-alpha)**t)/(alpha-beta)
print("pH closed-form err", np.abs(pH-pH_cf).max())
print("d closed-form err", np.abs(d-d_cf).max())
Delta = qM - qH
Delta_lb = (1-gamma)**t*(pM0-pH0)
print("Delta >= lower bound:", np.all(Delta >= Delta_lb-1e-12))
eH = qH - pH
eH_cf = a*alpha*((1-gamma)**t-(1-alpha)**t)/(alpha-gamma)
print("belief err closed-form err", np.abs(eH-eH_cf).max())

def h(p):
    p = np.clip(p,1e-12,1-1e-12)
    return -p*np.log2(p)-(1-p)*np.log2(1-p)
MI = h(pi*pM+(1-pi)*pH) - pi*h(pM) - (1-pi)*h(pH)
LR = pM/pH
LRhat = qM/qH
phi_true = pi*pM/(pi*pM+(1-pi)*pH)
phi_bel = pi*qM/(pi*qM+(1-pi)*qH)
TV = 0.5*(np.abs(pM-pH)+np.abs((1-pM)-(1-pH)))
Inat = MI*np.log(2)
print("bounds ok:", np.all(2*pi*(1-pi)*TV**2 <= Inat+1e-12), np.all(Inat <= 2*max(pi,1-pi)*TV+1e-12))
cost = 2.0*(pH-pH0)**2   # kappa_H = 2 illustrative
for k in [0,1,2,4,6,8,12,16,24,32]:
    print(k, f"{pH[k]:.3f} {pM[k]:.3f} LR={LR[k]:.2f} LRhat={LRhat[k]:.2f} MI={MI[k]:.4f} phi*={phi_true[k]:.3f} phi={phi_bel[k]:.3f}")

# LaTeX table
rows = [0,2,4,8,12,16,24,32]
with open("table_dynamics.tex","w") as f:
    f.write("\\begin{tabular}{@{}rccccccc@{}}\n\\toprule\n")
    f.write("$t$ & $p_H^t$ & $p_M^t$ & $\\operatorname{LR}_t$ & $\\widehat{\\operatorname{LR}}_t$ & $\\I_t$ (bits) & $\\phi_t^\\ast$ & $\\hat\\phi_t$ \\\\\n\\midrule\n")
    for k in rows:
        f.write(f"{k} & {pH[k]:.3f} & {pM[k]:.3f} & {LR[k]:.2f} & {LRhat[k]:.2f} & {MI[k]:.4f} & {phi_true[k]:.3f} & {phi_bel[k]:.3f} \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")

plt.rcParams.update({"font.size":9, "font.family":"serif"})
fig, ax = plt.subplots(1,2, figsize=(6.6,2.6))
ax[0].plot(t, LR, label="actual $\\mathrm{LR}_t$", lw=1.6, color="black")
ax[0].plot(t, LRhat, label="believed $\\widehat{\\mathrm{LR}}_t$", lw=1.6, ls="--", color="0.45")
ax[0].axhline(1, lw=0.6, color="0.7")
ax[0].set_xlabel("round $t$"); ax[0].set_ylabel("likelihood ratio"); ax[0].legend(frameon=False)
ax[0].set_xlim(0,T)
ax[1].plot(t, phi_true, label="calibrated $\\phi^\\ast_t$", lw=1.6, color="black")
ax[1].plot(t, phi_bel, label="reader's $\\hat\\phi_t$", lw=1.6, ls="--", color="0.45")
ax[1].axhline(pi, lw=0.6, color="0.7")
ax[1].set_xlabel("round $t$"); ax[1].set_ylabel("P(machine | feature present)"); ax[1].legend(frameon=False)
ax[1].set_xlim(0,T)
plt.tight_layout()
plt.savefig("fig_dynamics.pdf")
# find when actual LR within 5% of 1 and believed
for thr in [0.10, 0.05]:
    ta = int(np.argmax(LR-1 < thr)); tb = int(np.argmax(LRhat-1 < thr))
    print("LR-1 <",thr,": actual at t=",ta," believed at t=",tb)
