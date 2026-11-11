"""Builds every table and figure in the revised Extended Working Paper.

Run from the repo root:  python extended/paper_outputs.py [--online]
Writes extended/output/paper_tables.json and extended/output/figures/*.png.
--online adds the Statistics Canada FDI series (Table 7 rows, Appendix E); otherwise those rows are omitted.
"""
import io, json, os, sys, warnings, zipfile, urllib.request
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import GLSAR
from statsmodels.tsa.stattools import coint, acf
from statsmodels.stats.diagnostic import acorr_breusch_godfrey

OUT, FIG = "extended/output", "extended/output/figures"
os.makedirs(FIG, exist_ok=True)
base = pd.read_csv("data/fdi_data_1981_2018.csv", index_col="year")
ext = pd.read_csv("data/fdi_data_1981_2024.csv", index_col="year")
HAC = dict(cov_type="HAC", cov_kwds={"maxlags": 3})
PRIMARY = "dI ~ dX + U + FDI + FDI_l1"
f3 = lambda v: (f"{v:.3f}" if round(v, 3) != 0 else "0.000").replace("-", "−")
fp = lambda p: "<0.001" if p < 0.001 else f"{p:.3f}"
ci = lambda lo, hi: f"[{f3(lo)}, {f3(hi)}]"


def prep(raw, unit="cad", x="Y"):
    d = raw.copy()
    d["I"], d["U"], d["FDI"], d["Y"] = d[f"I_{unit}"], d[f"U_{unit}"], d[f"FDI_{unit}"], d[f"Y_{unit}"]
    d["N"] = d["Y"] - d["I"]
    d["X"] = d[x]
    d["dI"], d["dX"] = d["I"].diff(), d["X"].diff()
    d["FDI_l1"] = d["FDI"].shift(1)
    d["dI_l1"], d["dX_l1"] = d["dI"].shift(1), d["dX"].shift(1)
    d["ECT"] = smf.ols("I ~ X", data=d).fit().resid.shift(1)
    d["S"] = -d["gap_pct"]
    d["t"] = np.arange(len(d))
    for yr in (2001, 2009, 2015, 2020):
        d[f"y{yr}"] = (d.index == yr).astype(int)
    return d


def bg(m):
    return acorr_breusch_godfrey(sm.OLS(m.model.endog, m.model.exog).fit(), nlags=2)[1]


def summ(m):
    t = m.t_test("FDI + FDI_l1 = 0"); lo, hi = t.conf_int()[0]
    return dict(d0=m.params["FDI"], d1=m.params["FDI_l1"], s=float(t.effect[0]), lo=lo, hi=hi,
                p_sum=float(t.pvalue), p_d1=m.wald_test("FDI_l1 = 0", scalar=True).pvalue, bg=bg(m), n=int(m.nobs))


def row_sum(label, r, extra=None):
    return [label, f3(r["d0"]), f3(r["d1"]), f"{f3(r['s'])} {ci(r['lo'], r['hi'])}", fp(r["p_sum"]), fp(r["bg"]), str(r["n"])] + (extra or [])


T, TXT = {}, {}

# ---------- Table 4: cointegration --------------------------------------------------------
rows = []
for raw, smp in ((base, "1981–2018"), (ext, "1981–2024")):
    for unit, cur in (("cad", "CAD"), ("usd", "USD")):
        for x, lab in (("Y", "Total (Y)"), ("N", "Excl. business investment (N)")):
            d = prep(raw, unit, x)
            rows.append([smp, cur, lab, fp(coint(d.I, d.X, trend="c")[1]),
                         fp(coint(d.I, d.X, trend="c", maxlag=3, autolag="bic")[1])])
T["t4"] = dict(header=["Sample", "Currency", "Expenditure", "Default AIC p", "BIC cap 3 p"], rows=rows,
               widths=[1500, 1100, 2900, 1700, 1700])

# ---------- Table 5: baseline C$ estimates -------------------------------------------------
specs = [("(1) Total expenditure", "Y", ""), ("(2) Excl. investment", "N", ""),
         ("(3) (1) + trend", "Y", " + t"), ("(4) (2) + trend", "N", " + t")]
fits = [(lab, smf.ols(PRIMARY + extra, data=prep(base, x=x)).fit(**HAC)) for lab, x, extra in specs]
names = [("dX", "Expenditure change, ΔX"), ("U", "Capacity slack, U"), ("FDI", "FDI, current (δ₀)"),
         ("FDI_l1", "FDI, lagged (δ₁)"), ("t", "Linear trend"), ("Intercept", "Intercept")]
rows = []
for k, lab in names:
    rows.append([lab] + [f3(m.params[k]) if k in m.params else "—" for _, m in fits])
    rows.append([""] + [f"({m.bse[k]:.3f})" if k in m.params else "" for _, m in fits])
S = [summ(m) for _, m in fits]
rows += [["Coefficient sum δ₀ + δ₁"] + [f3(r["s"]) for r in S],
         ["   95% interval"] + [ci(r["lo"], r["hi"]) for r in S],
         ["p, δ₀ + δ₁ = 0"] + [fp(r["p_sum"]) for r in S],
         ["p, δ₁ = 0"] + [fp(r["p_d1"]) for r in S],
         ["Breusch–Godfrey p"] + [fp(r["bg"]) for r in S],
         ["Observations"] + [str(r["n"]) for r in S]]
T["t5"] = dict(header=["Regressor"] + [l for l, _ in fits], rows=rows, widths=[2700, 1600, 1600, 1600, 1600])
TXT["primary"] = {lab: {k: float(v) for k, v in m.params.items()} | {"p_" + k: float(v) for k, v in m.pvalues.items()} | summ(m)
                  for lab, m in fits}

# ---------- Table 6: levels benchmark in both currencies ----------------------------------
cols = []
for unit, cur in (("usd", "US$"), ("cad", "C$")):
    d = prep(base, unit)
    cols.append((f"{cur} OLS", smf.ols("I ~ Y + U + FDI", data=d).fit()))
    cols.append((f"{cur} AR(1)", GLSAR.from_formula("I ~ Y + U + FDI", data=d, rho=1).iterative_fit(maxiter=50)))
rows = []
for k, lab in (("Y", "Expenditure, Y"), ("U", "Capacity slack, U"), ("FDI", "FDI"), ("Intercept", "Intercept")):
    rows.append([lab] + [f3(m.params[k]) for _, m in cols])
    rows.append([""] + [f"({m.bse[k]:.3f})" for _, m in cols])
rows.append(["FDI p-value"] + [fp(m.pvalues["FDI"]) for _, m in cols])
rows.append(["Observations"] + [str(int(m.nobs)) for _, m in cols])
T["t6"] = dict(header=["Regressor"] + [l for l, _ in cols], rows=rows, widths=[2700, 1600, 1600, 1600, 1600])
TXT["levels"] = {l: dict(fdi=float(m.params["FDI"]), p=float(m.pvalues["FDI"])) for l, m in cols}

# ---------- Table 7: sensitivity of the coefficient sum ------------------------------------
rows, fig2 = [], []


def add(label, model, short=None, group="C$"):
    r = summ(model); rows.append(row_sum(label, r)); fig2.append((short or label, r, group)); return r


add("Baseline (X = Y)", smf.ols(PRIMARY, data=prep(base)).fit(**HAC), "Baseline, X = Y")
add("Baseline (X = N)", smf.ols(PRIMARY, data=prep(base, x="N")).fit(**HAC), "Baseline, X = N")
add("+ linear trend (X = Y)", smf.ols(PRIMARY + " + t", data=prep(base)).fit(**HAC), "Trend, X = Y")
add("+ linear trend (X = N)", smf.ols(PRIMARY + " + t", data=prep(base, x="N")).fit(**HAC), "Trend, X = N")
add("ECM variant (X = Y)", smf.ols(PRIMARY + " + ECT", data=prep(base)).fit(**HAC), "ECM, X = Y")
add("ECM variant (X = N)", smf.ols(PRIMARY + " + ECT", data=prep(base, x="N")).fit(**HAC), "ECM, X = N")
add("1981–2024 + 2020 indicator (X = Y)", smf.ols(PRIMARY + " + y2020", data=prep(ext)).fit(**HAC), "To 2024, X = Y")
add("1981–2024 + 2020 indicator (X = N)", smf.ols(PRIMARY + " + y2020", data=prep(ext, x="N")).fit(**HAC), "To 2024, X = N")
cs = prep(base).dropna(subset=["dI_l1", "dX_l1", "FDI_l1", "dI", "dX"])
add("Common 1983–2018 sample (X = Y)", smf.ols(PRIMARY, data=cs).fit(**HAC), group="skip")
add("   + lagged ΔX", smf.ols(PRIMARY + " + dX_l1", data=cs).fit(**HAC), group="skip")
add("   + lagged ΔI and ΔX", smf.ols(PRIMARY + " + dI_l1 + dX_l1", data=cs).fit(**HAC), "Lagged ΔI, ΔX, X = Y")
csn = prep(base, x="N").dropna(subset=["dI_l1", "dX_l1", "FDI_l1", "dI", "dX"])
add("   + lagged ΔI and ΔX (X = N)", smf.ols(PRIMARY + " + dI_l1 + dX_l1", data=csn).fit(**HAC), "Lagged ΔI, ΔX, X = N")

if "--online" in sys.argv:
    def statcan(table):
        raw = urllib.request.urlopen(f"https://www150.statcan.gc.ca/n1/tbl/csv/{table}-eng.zip", timeout=300).read()
        return pd.read_csv(zipfile.ZipFile(io.BytesIO(raw)).open(f"{table}.csv"), low_memory=False)
    a = statcan("36100471")
    liab = (a[(a.GEO == "Canada") & (a["Financial account"] == "Direct investment liabilities")
              & (a["Countries or regions"] == "All countries")]
            .assign(year=lambda z: z.REF_DATE.astype(int)).set_index("year")["VALUE"] / 1000)
    q = statcan("36100442")
    q = q[(q["Asset liability and directional direct investment presentations"]
           == "Equals: Foreign direct investment in Canada (directional presentation)") & (q["Geographic region"] == "All countries")]
    q = q.assign(year=q.REF_DATE.str[:4].astype(int))
    directional = (q.groupby("year")["VALUE"].sum() / 1000)[q.groupby("year").size() == 4]
    url = "https://api.worldbank.org/v2/country/CAN/indicator/{}?format=json&date=1981:2024&per_page=100"
    wbget = lambda c: pd.Series({int(r["date"]): r["value"] for r in json.load(urllib.request.urlopen(url.format(c), timeout=60))[1]}).sort_index()
    wb_cad = wbget("BX.KLT.DINV.CD.WD") * wbget("PA.NUS.FCRF") / 1e9

    def alt(ser, start):
        z = base.loc[start:2018].copy(); z["FDI_cad"] = ser.reindex(z.index); return z
    add("StatCan direct investment liabilities (X = Y)", smf.ols(PRIMARY, data=prep(alt(liab, 1981))).fit(**HAC), "StatCan liabilities")
    add("Archived FDI, 1991–2018 (X = Y)", smf.ols(PRIMARY, data=prep(alt(base["FDI_cad"], 1990))).fit(**HAC), "Archived, 1991–2018")
    add("StatCan directional inward FDI, 1991–2018 (X = Y)", smf.ols(PRIMARY, data=prep(alt(directional, 1990))).fit(**HAC), "StatCan directional, 1991–2018")
    rowsE = []
    for yr in (2007, 2009, 2015, 2018, 2024):
        rowsE.append([str(yr), f"{wb_cad[yr]:.3f}", f"{liab[yr]:.3f}", f"{directional[yr]:.3f}"])
    T["tE1"] = dict(header=["Year", "World Bank × annual FX", "StatCan liabilities", "StatCan directional inward"],
                    rows=rowsE, widths=[1200, 2600, 2600, 2600])
    dd = (wb_cad - liab).loc[1981:2018]
    TXT["fdi_compare"] = dict(corr=float(wb_cad.loc[1981:2018].corr(liab.loc[1981:2018])), mad=float(dd.abs().mean()),
                              maxd=float(dd.abs().max()), maxyr=int(dd.abs().idxmax()),
                              archived_corr=float(base["FDI_cad"].corr(liab.loc[1981:2018])))

add("US$ change equation (two-term)", smf.ols(PRIMARY, data=prep(base, "usd")).fit(**HAC), "US$ change equation", "US$")
add("US$ ECM (two-term)", smf.ols(PRIMARY + " + ECT", data=prep(base, "usd")).fit(**HAC), "US$ ECM", "US$")
T["t7"] = dict(header=["Specification", "δ₀", "δ₁", "δ₀ + δ₁ [95% CI]", "p (sum)", "BG p", "n"], rows=rows,
               widths=[3300, 750, 750, 2150, 850, 750, 500])

# contemporaneous-only rows, for the text
TXT["contemp"] = {}
for lab, raw, x, extra in (("Y", base, "Y", ""), ("N", base, "N", ""), ("2024Y", ext, "Y", " + y2020")):
    m = smf.ols("dI ~ dX + U + FDI" + extra, data=prep(raw, x=x)).fit(**HAC)
    TXT["contemp"][lab] = dict(b=float(m.params["FDI"]), p=float(m.pvalues["FDI"]))
TXT["hac"] = {}
for L in (1, 3, 4):
    m = smf.ols(PRIMARY, data=prep(base)).fit(cov_type="HAC", cov_kwds={"maxlags": L}); r = summ(m)
    TXT["hac"][L] = [r["lo"], r["hi"], r["p_sum"]]
est = prep(base)[["dI", "dX", "U", "FDI", "FDI_l1"]].dropna()
loo = pd.Series({yr: smf.ols(PRIMARY, data=est.drop(yr)).fit().params[["FDI", "FDI_l1"]].sum() for yr in est.index})
TXT["loo"] = [float(loo.min()), int(loo.idxmin()), float(loo.max()), int(loo.idxmax())]

# ---------- Table 8: currency bridge -------------------------------------------------------
import itertools


def bridge_fit(ops, x="Y", lag=True):
    b = base.copy(); e = b["fx"]
    xu = b["Y_usd"] if x == "Y" else b["Y_usd"] - b["I_usd"]
    xc = b["Y_cad"] if x == "Y" else b["Y_cad"] - b["I_cad"]
    y = b["I_cad"].diff() if "V" in ops else e * b["I_usd"].diff()
    X = pd.DataFrame({"dX": xc.diff() if "V" in ops else e * xu.diff(), "U": b["U_cad"], "FDI": b["FDI_cad"]})
    if lag:
        X["FDI_l1"] = b["FDI_cad"].shift(1) * (1 if "L" in ops else e / e.shift(1))
    if "E" not in ops:
        X["e"] = e
    if "C" in ops:
        X = sm.add_constant(X)
    df = pd.concat([y.rename("y"), X, (e ** -2).rename("w")], axis=1).dropna()
    m = sm.WLS(df["y"], df[X.columns], weights=np.ones(len(df)) if "W" in ops else df["w"]).fit()
    return m.params["FDI"] + (m.params["FDI_l1"] if lag else 0)


def shapley(x="Y", lag=True):
    ops = list("WCVLE") if lag else list("WCVE")
    val = {frozenset(s): bridge_fit(s, x, lag) for k in range(len(ops) + 1) for s in itertools.combinations(ops, k)}
    contrib = {op: [] for op in ops}
    for p in itertools.permutations(ops):
        cur = frozenset()
        for op in p:
            nxt = cur | {op}; contrib[op].append(val[nxt] - val[cur]); cur = nxt
    return val[frozenset()], val[frozenset(ops)], {op: (np.mean(v), min(v), max(v)) for op, v in contrib.items()}


B = [shapley("Y"), shapley("N"), shapley("Y", lag=False)]
lab = {"W": "W: remove weights", "C": "C: add ordinary constant", "V": "V: C$ changes (remove revaluation)",
       "L": "L: unadjusted lagged FDI", "E": "E: remove eₜ"}
fmt = lambda t: f"{f3(t[0])} [{f3(t[1])}, {f3(t[2])}]"
rows = [["Start: exact US$ translation"] + [f3(b[0]) for b in B]]
for op in "WCVLE":
    rows.append([lab[op]] + [fmt(b[2][op]) if op in b[2] else "—" for b in B])
rows.append(["End: C$ estimate"] + [f3(b[1]) for b in B])
T["t8"] = dict(header=["Adjustment", "Two-term, X = Y", "Two-term, X = N", "Current FDI only, X = Y"], rows=rows,
               widths=[3200, 2000, 2000, 2000])

e, el = base["fx"], base["fx"].shift(1)
A = base["I_cad"].diff() / e; R = base["I_cad"].shift(1) * (1 / e - 1 / el); dIu = base["I_usd"].diff()
v = pd.DataFrame({"A": A, "R": R, "u": dIu}).dropna()
TXT["reval"] = dict(vA=v.A.var() / v.u.var(), vR=v.R.var() / v.u.var(), cov2=2 * v.A.cov(v.R) / v.u.var(),
                    corr=v.A.corr(v.R), r2=np.corrcoef(v.A, v.u)[0, 1] ** 2)

# ---------- Table 9 and 10: capacity interaction -------------------------------------------
rows, rows10, TXT["inter"] = [], [], {}
INT = PRIMARY + " + S + FDI:S + FDI_l1:S"
for x, xl in (("Y", "Total expenditure (Y)"), ("N", "Excl. investment (N)")):
    dd = prep(base, x=x); m = smf.ols(INT, data=dd).fit(**HAC)
    ts = m.t_test("FDI:S + FDI_l1:S = 0"); slo, shi = ts.conf_int()[0]
    cc = m.conf_int()
    rows.append([xl, f"{f3(m.params['FDI:S'])} {ci(*cc.loc['FDI:S'])}", f"{f3(m.params['FDI_l1:S'])} {ci(*cc.loc['FDI_l1:S'])}",
                 fp(m.wald_test("FDI:S = 0, FDI_l1:S = 0", scalar=True).pvalue),
                 f"{f3(float(ts.effect[0]))} {ci(slo, shi)}", fp(float(ts.pvalue)), fp(bg(m))])
    if x == "Y":
        s_est = dd.loc[m.model.data.row_labels, "S"]
        for q in (0.25, 0.5, 0.75):
            s = s_est.quantile(q); cells = [f"{int(q*100)}th", f"{s:.2f}".replace("-", "−")]
            for expr in (f"FDI + {s:.6f}*FDI:S", f"FDI_l1 + {s:.6f}*FDI_l1:S", f"FDI + FDI_l1 + {s:.6f}*FDI:S + {s:.6f}*FDI_l1:S"):
                t = m.t_test(f"{expr} = 0"); lo, hi = t.conf_int()[0]; cells.append(f"{f3(float(t.effect[0]))} {ci(lo, hi)}")
            rows10.append(cells)
    r = smf.ols("dI ~ dX + S + FDI + FDI:S", data=dd).fit(**HAC)
    u = smf.ols(PRIMARY + " + FDI:U + FDI_l1:U", data=dd).fit(**HAC)
    TXT["inter"][x] = dict(restricted=float(r.params["FDI:S"]), restricted_p=float(r.pvalues["FDI:S"]),
                           nominal_joint=float(u.wald_test("FDI:U = 0, FDI_l1:U = 0", scalar=True).pvalue))
T["t9"] = dict(header=["Expenditure control", "η₀ (FDI × S)", "η₁ (FDI₋₁ × S)", "Joint p", "η₀ + η₁", "p (η₀ + η₁)", "BG p"],
               rows=rows, widths=[1900, 1900, 1900, 800, 1900, 900, 700])
T["t10"] = dict(header=["Slack percentile", "S (%)", "Current FDI", "Lagged FDI", "Sum"], rows=rows10,
                widths=[1400, 900, 2300, 2300, 2300])

# ---------- Appendix D: downturn indicators --------------------------------------------------
rows, rowsD2 = [], []
d = prep(base)
for label, extra in (("None (baseline)", ""), ("2009", " + y2009"), ("2001 and 2009", " + y2001 + y2009"),
                     ("2001, 2009 and 2015", " + y2001 + y2009 + y2015")):
    rows.append(row_sum(label, summ(smf.ols(PRIMARY + extra, data=d).fit(**HAC))))
T["tD1"] = dict(header=["Indicators added", "δ₀", "δ₁", "δ₀ + δ₁ [95% CI]", "p (sum)", "BG p", "n"], rows=rows,
                widths=[2700, 800, 800, 2300, 900, 800, 600])
for x in ("Y", "N"):
    dd = prep(base, x=x); est_i = dd[["dI", "dX", "U", "FDI", "FDI_l1", "S", "y2001", "y2009", "y2015"]].dropna()
    for label, data, extra in (("Baseline", dd, ""), ("+ 2009", dd, " + y2009"), ("+ 2001, 2009", dd, " + y2001 + y2009"),
                               ("+ 2001, 2009, 2015", dd, " + y2001 + y2009 + y2015"),
                               ("Omit 2009", est_i.drop(2009), ""), ("Omit 2001", est_i.drop(2001), "")):
        m = smf.ols(INT + extra, data=data).fit(**HAC); cc = m.conf_int()
        ts = m.t_test("FDI:S + FDI_l1:S = 0"); slo, shi = ts.conf_int()[0]
        rowsD2.append([x, label, f"{f3(m.params['FDI:S'])} {ci(*cc.loc['FDI:S'])}", f"{f3(m.params['FDI_l1:S'])} {ci(*cc.loc['FDI_l1:S'])}",
                       fp(m.wald_test("FDI:S = 0, FDI_l1:S = 0", scalar=True).pvalue), f"{f3(float(ts.effect[0]))} {ci(slo, shi)}",
                       fp(float(ts.pvalue))])
T["tD2"] = dict(header=["X", "Check", "η₀ [95% CI]", "η₁ [95% CI]", "Joint p", "η₀ + η₁ [95% CI]", "p (η₀ + η₁)"],
                rows=rowsD2, widths=[450, 1700, 2000, 2000, 800, 2000, 900])

# ---------- Table A1: sample accounting ---------------------------------------------------
T["tA1"] = dict(header=["Specification", "1981–2018", "1981–2024", "First usable year"], rows=[
    ["Levels", "38", "44", "1981"],
    ["Baseline change equation (current and lagged FDI) and ECM variant", "37", "43", "1982"],
    ["Common-sample dynamic comparison", "36", "42", "1983"],
    ["Directional-FDI comparison (StatCan, from 1990)", "28", "—", "1991"]], widths=[4600, 1400, 1400, 1800])

# ---------- Figures ----------------------------------------------------------------------
BLUE, ORANGE, GRAY = "#1f5a84", "#b7642d", "#7b878c"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.6, 5.4), sharex=True)
a1.plot(base.index, base["I_cad"], color=BLUE, lw=1.8, label="Business investment")
a1.plot(base.index, base["FDI_cad"], color=ORANGE, lw=1.8, label="FDI net inflows")
a1.set_ylabel("Current C$ billions"); a1.legend(frameon=False, loc="upper left")
a2.bar(base.index, base["gap_pct"], color=GRAY); a2.axhline(0, color="black", lw=0.8)
a2.set_ylabel("Output gap (%)"); a2.set_xlabel("Year")
fig.tight_layout(); fig.savefig(f"{FIG}/figure1_series_cad.png", dpi=200); plt.close(fig)

f2 = [z for z in fig2 if z[2] != "skip"]
fig, ax = plt.subplots(figsize=(7.6, 0.36 * len(f2) + 0.9))
ys = np.arange(len(f2))[::-1]
for y, (name, r, g) in zip(ys, f2):
    c = ORANGE if g == "US$" else BLUE
    ax.plot([r["lo"], r["hi"]], [y, y], color=c, lw=1.6)
    ax.plot(r["s"], y, "o", color=c, ms=5)
ax.axvline(0, color="gray", lw=0.8)
ax.set_yticks(ys, [z[0] for z in f2]); ax.set_xlabel("FDI coefficient sum δ₀ + δ₁ with 95% interval")
fig.tight_layout(); fig.savefig(f"{FIG}/figure2_coefficient_sums.png", dpi=200); plt.close(fig)

m_c = smf.ols(PRIMARY, data=prep(base)).fit()
m_u = smf.ols("dI ~ dX + U + FDI + ECT", data=prep(base, "usd")).fit()
fig, axs = plt.subplots(1, 2, figsize=(7.6, 2.9), sharey=True)
for ax, m, title in ((axs[0], m_c, "C$ baseline change equation"), (axs[1], m_u, "Earlier US$ ECM (current FDI only)")):
    r = acf(m.resid, nlags=6, fft=False)[1:]; band = 1.96 / np.sqrt(len(m.resid))
    ax.bar(range(1, 7), r, color=BLUE, width=0.5); ax.axhline(0, color="black", lw=0.8)
    ax.axhspan(-band, band, color=BLUE, alpha=0.15, lw=0); ax.set_title(title, fontsize=10); ax.set_xlabel("Lag")
axs[0].set_ylabel("Residual autocorrelation")
fig.tight_layout(); fig.savefig(f"{FIG}/figure3_residual_acf.png", dpi=200); plt.close(fig)

json.dump(dict(tables=T, text=TXT), open(f"{OUT}/paper_tables.json", "w"), indent=1, default=float, ensure_ascii=False)
print("tables:", list(T)); print(json.dumps(TXT, indent=1, default=float)[:6000])
