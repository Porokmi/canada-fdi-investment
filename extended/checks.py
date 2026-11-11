"""Reproduces every number in the revised Extended Working Paper.

Run from the repo root:  python extended/checks.py  [--online]
Uses only the archived CSVs in data/. C$ is the primary currency; HAC(3) unless stated.
"""
import itertools, math, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller, coint
from statsmodels.stats.diagnostic import acorr_breusch_godfrey

base = pd.read_csv("data/fdi_data_1981_2018.csv", index_col="year")
ext = pd.read_csv("data/fdi_data_1981_2024.csv", index_col="year")
HAC = dict(cov_type="HAC", cov_kwds={"maxlags": 3})
fmt_p = lambda p: "<0.001" if p < 0.001 else f"{p:.3f}"


def prep(raw, unit="cad", x="Y"):
    d = raw.copy()
    d["I"], d["U"], d["FDI"], d["Y"] = d[f"I_{unit}"], d[f"U_{unit}"], d[f"FDI_{unit}"], d[f"Y_{unit}"]
    d["N"] = d["Y"] - d["I"]
    d["X"] = d[x]
    d["dI"], d["dX"] = d["I"].diff(), d["X"].diff()
    d["FDI_l1"] = d["FDI"].shift(1)
    d["dI_l1"], d["dX_l1"] = d["dI"].shift(1), d["dX"].shift(1)
    d["ECT"] = smf.ols("I ~ X", data=d).fit().resid.shift(1)
    d["S"] = -d["gap_pct"]                      # percent slack, positive = below potential
    d["t"] = np.arange(len(d))
    for yr in (2001, 2009, 2015, 2020):
        d[f"y{yr}"] = (d.index == yr).astype(int)
    return d


def bg(m):
    return acorr_breusch_godfrey(sm.OLS(m.model.endog, m.model.exog).fit(), nlags=2)[1]


def two_term(m):
    t = m.t_test("FDI + FDI_l1 = 0")
    lo, hi = t.conf_int()[0]
    return dict(d0=m.params["FDI"], d1=m.params["FDI_l1"],
                p_d1=m.wald_test("FDI_l1 = 0", scalar=True).pvalue,
                p_sum=float(t.pvalue), sum=float(t.effect[0]), lo=lo, hi=hi, bg=bg(m), n=int(m.nobs))


def show_two_term(label, r):
    print(f"  {label:<28} d0={r['d0']: .3f} d1={r['d1']: .3f}  p(d1=0)={fmt_p(r['p_d1'])}  "
          f"p(sum=0)={fmt_p(r['p_sum'])}  sum={r['sum']: .3f} [{r['lo']: .3f}, {r['hi']: .3f}]  "
          f"BG={fmt_p(r['bg'])}  n={r['n']}")


PRIMARY = "dI ~ dX + U + FDI + FDI_l1"

print("=" * 100)
print("A. Sample and units (Section 5.4)")
d = prep(base)
print(f"  primary-equation sample: {d[['dI','dX','U','FDI','FDI_l1']].dropna().index.min()}-"
      f"{d[['dI','dX','U','FDI','FDI_l1']].dropna().index.max()}, n={len(d[['dI','dX','U','FDI','FDI_l1']].dropna())}")
print(f"  extended sample n={len(prep(ext)[['dI','dX','U','FDI','FDI_l1']].dropna())}")
print(f"  common sample with lagged dI, dX: {d[['dI_l1','dX_l1','FDI_l1']].dropna().index.min()}-2018, "
      f"n={len(d[['dI','dI_l1','dX_l1','FDI_l1']].dropna())}")
print("  units: I_cad, Y_cad, U_cad, FDI_cad in current C$ billions; gap_pct in percent of potential")

print("\nB. ADF tests, C$, 1981-2018 (Section 5.3)")
for v in ["I_cad", "Y_cad", "U_cad", "FDI_cad"]:
    c = adfuller(base[v], regression="c", autolag="AIC")[1]
    ct = adfuller(base[v], regression="ct", autolag="AIC")[1]
    dc = adfuller(base[v].diff().dropna(), regression="c", autolag="AIC")[1]
    print(f"  {v:<8} const p={fmt_p(c)}  const+trend p={fmt_p(ct)}  first diff p={fmt_p(dc)}")
m = smf.ols("FDI ~ t", data=d).fit(**HAC)
print(f"  FDI_cad linear trend: {m.params['t']:.3f} bn/yr, p={fmt_p(m.pvalues['t'])}")

print("\nC. Engle-Granger cointegration p, default AIC / BIC cap 3 (Section 5.5)")
for x in ["Y", "N"]:
    cells = []
    for raw in (base, ext):
        dd = prep(raw, x=x)
        cells.append(f"{coint(dd['I'], dd['X'], trend='c')[1]:.3f} / "
                     f"{fmt_p(coint(dd['I'], dd['X'], trend='c', maxlag=3, autolag='bic')[1])}")
    print(f"  I ~ {x}:  1981-2018 {cells[0]}   1981-2024 {cells[1]}")

print("\nD. Primary model and checks, C$")
rows = {}
for x in ["Y", "N"]:
    dm, de = prep(base, x=x), prep(ext, x=x)
    rows[f"Primary (X = {x})"] = two_term(smf.ols(PRIMARY, data=dm).fit(**HAC))
    rows[f"+ linear trend ({x})"] = two_term(smf.ols(PRIMARY + " + t", data=dm).fit(**HAC))
    rows[f"ECM variant ({x})"] = two_term(smf.ols(PRIMARY + " + ECT", data=dm).fit(**HAC))
    rows[f"2024 + 2020 dummy ({x})"] = two_term(smf.ols(PRIMARY + " + y2020", data=de).fit(**HAC))
for k, r in rows.items():
    show_two_term(k, r)
neg = sum(r["sum"] < 0 for r in rows.values()); sig = sum(r["p_sum"] < 0.05 for r in rows.values())
print(f"  -> sum negative in {neg}/{len(rows)}, significant at 5% in {sig}/{len(rows)}")

print("\nE. Exploratory downturn indicators and leave-one-out (X = Y)")
d = prep(base)
for label, extra in [("2009", " + y2009"), ("2001 and 2009", " + y2001 + y2009"),
                     ("2001, 2009 and 2015", " + y2001 + y2009 + y2015")]:
    show_two_term(label, two_term(smf.ols(PRIMARY + extra, data=d).fit(**HAC)))
est = d[["dI", "dX", "U", "FDI", "FDI_l1"]].dropna()
loo = pd.Series({yr: smf.ols(PRIMARY, data=est.drop(yr)).fit().params[["FDI", "FDI_l1"]].sum() for yr in est.index})
print(f"  leave-one-out sum: min {loo.min():.3f} (drop {loo.idxmin()}), max {loo.max():.3f} (drop {loo.idxmax()})")

print("\nF. Contemporaneous-only C$ change equation (imposes d1 = 0)")
for label, raw, x, extra in [("1981-2018, Y", base, "Y", ""), ("1981-2018, N", base, "N", ""),
                             ("1981-2024, Y + 2020", ext, "Y", " + y2020")]:
    m = smf.ols("dI ~ dX + U + FDI" + extra, data=prep(raw, x=x)).fit(**HAC)
    print(f"  {label:<22} FDI={m.params['FDI']: .3f} p={fmt_p(m.pvalues['FDI'])} BG={fmt_p(bg(m))}")

print("\nG. HAC bandwidth sensitivity, primary (X = Y)")
for L in (1, 3, 4):
    r = two_term(smf.ols(PRIMARY, data=prep(base)).fit(cov_type="HAC", cov_kwds={"maxlags": L}))
    print(f"  maxlags={L}: sum={r['sum']:.3f} [{r['lo']:.3f}, {r['hi']:.3f}] p={fmt_p(r['p_sum'])}")

print("\nH. Lagged dI and dX on a common 1983-2018 sample")
for x in ["Y", "N"]:
    dd = prep(base, x=x).dropna(subset=["dI_l1", "dX_l1", "FDI_l1", "dI", "dX"])
    for label, extra in [("baseline (common sample)", ""), ("+ lag dX", " + dX_l1"), ("+ lag dI and dX", " + dI_l1 + dX_l1")]:
        show_two_term(f"{x}: {label}", two_term(smf.ols(PRIMARY + extra, data=dd).fit(**HAC)))

print("\nI. Revaluation decomposition of the US$ investment change, 1982-2018")
e, el = base["fx"], base["fx"].shift(1)
A = base["I_cad"].diff() / e                       # C$ spending change converted at today's rate
R = base["I_cad"].shift(1) * (1 / e - 1 / el)      # revaluation of last year's level
dIu = base["I_usd"].diff()
assert (A + R - dIu).abs().max() < 1e-9
v = pd.DataFrame({"A": A, "R": R, "dIu": dIu}).dropna()
vu, va, vr, cov = v.dIu.var(), v.A.var(), v.R.var(), v.A.cov(v.R)
print(f"  Var(dI_usd)={vu:.1f} = Var(A) {va:.1f} + Var(R) {vr:.1f} + 2Cov {2*cov:.1f}")
print(f"  Var(R)/Var(dI_usd)={vr/vu:.3f}  Var(A)/Var(dI_usd)={va/vu:.3f}  2Cov/Var(dI_usd)={2*cov/vu:.3f}  corr(A,R)={v.A.corr(v.R):.3f}")
print(f"  R-squared of dI_usd on A alone: {np.corrcoef(v.A, v.dIu)[0,1]**2:.3f}")
print(f"  2015: dI_cad={base.I_cad.diff()[2015]:.1f}, dI_usd={dIu[2015]:.1f}, A={A[2015]:.1f}, R={R[2015]:.1f}, "
      f"fx {el[2015]:.3f} -> {e[2015]:.3f}")

print("\nJ. Currency bridge, all 2^k adjustment sets, Shapley attribution over orders")
OPS_FULL = {"W": "remove weights", "C": "add constant", "V": "C$ changes (drop revaluation)",
            "L": "unadjusted lagged FDI", "E": "drop e_t"}


def bridge_fit(ops, x="Y", lag=True):
    b = base.copy(); e = b["fx"]
    xu = b["Y_usd"] if x == "Y" else b["Y_usd"] - b["I_usd"]
    xc = b["Y_cad"] if x == "Y" else b["Y_cad"] - b["I_cad"]
    y = b["I_cad"].diff() if "V" in ops else e * b["I_usd"].diff()
    X = pd.DataFrame({"dX": xc.diff() if "V" in ops else e * xu.diff(),
                      "U": b["U_cad"], "FDI": b["FDI_cad"]})
    if lag:
        X["FDI_l1"] = b["FDI_cad"].shift(1) * (1 if "L" in ops else e / e.shift(1))
    if "E" not in ops:
        X["e"] = e
    if "C" in ops:
        X = sm.add_constant(X)
    df = pd.concat([y.rename("y"), X, (e ** -2).rename("w")], axis=1).dropna()
    w = np.ones(len(df)) if "W" in ops else df["w"]
    m = sm.WLS(df["y"], df[X.columns], weights=w).fit()
    return m.params["FDI"] + (m.params["FDI_l1"] if lag else 0), m


BRIDGE_ROWS = []


def bridge(x="Y", lag=True):
    ops = list("WCVLE") if lag else list("WCVE")
    val = {}
    for k in range(len(ops) + 1):
        for s in itertools.combinations(ops, k):
            v, m = bridge_fit(s, x, lag)
            val[frozenset(s)] = v
            ex = m.model.exog
            BRIDGE_ROWS.append(dict(model="two-term" if lag else "contemporaneous", X=x, adjustments="".join(s) or "none",
                                    n=int(m.nobs), k=ex.shape[1], rank=int(np.linalg.matrix_rank(ex)),
                                    cond=float(np.linalg.cond(ex)), fdi_sum=v))
    bad = [r for r in BRIDGE_ROWS if r["model"] == ("two-term" if lag else "contemporaneous") and r["X"] == x and r["rank"] < r["k"]]
    print(f"  [{len(val)} combinations fitted; rank-deficient designs: {len(bad)}]")
    # check endpoints against directly estimated equations
    usd = smf.ols(("dI ~ dX + U + FDI" + (" + FDI_l1" if lag else "")), data=prep(base, "usd", x)).fit()
    cad = smf.ols(("dI ~ dX + U + FDI" + (" + FDI_l1" if lag else "")), data=prep(base, "cad", x)).fit()
    tgt = lambda m: m.params["FDI"] + (m.params["FDI_l1"] if lag else 0)
    print(f"  [{'two-term' if lag else 'contemporaneous-only'}, X={x}]  exact translation {val[frozenset()]:.4f} "
          f"(US$ direct {tgt(usd):.4f});  all adjustments {val[frozenset(ops)]:.4f} (C$ direct {tgt(cad):.4f})")
    seq = []; cur = set()
    for op in ops:
        cur.add(op); seq.append(f"{op}:{val[frozenset(cur)]:.3f}")
    print(f"    stated order {' -> '.join(seq)}")
    shap = {op: 0.0 for op in ops}
    perms = list(itertools.permutations(ops))
    for p in perms:
        cur = frozenset()
        for op in p:
            nxt = cur | {op}; shap[op] += (val[nxt] - val[cur]) / len(perms); cur = nxt
    rng = {op: [] for op in ops}
    for p in perms:
        cur = frozenset()
        for op in p:
            nxt = cur | {op}; rng[op].append(val[nxt] - val[cur]); cur = nxt
    for op in ops:
        print(f"    {OPS_FULL[op]:<32} Shapley {shap[op]: .3f}   range over orders [{min(rng[op]): .3f}, {max(rng[op]): .3f}]")


bridge("Y", lag=False)
bridge("Y", lag=True)
bridge("N", lag=True)
import os
os.makedirs("extended/output", exist_ok=True)
br = pd.DataFrame(BRIDGE_ROWS)
br.to_csv("extended/output/bridge_combinations.csv", index=False)
print(f"  saved {len(br)} model outputs to extended/output/bridge_combinations.csv; "
      f"all full rank: {bool((br['rank'] == br['k']).all())}; max condition number {br['cond'].max():.0f}")
print("  levels control (contemporaneous-only levels regression):")
b = base; e = b["fx"]
Xc = pd.DataFrame({"e": e, "Y": b["Y_cad"], "U": b["U_cad"], "FDI": b["FDI_cad"]})
print(f"    US$ OLS {sm.OLS(b['I_usd'], sm.add_constant(b[['Y_usd','U_usd','FDI_usd']])).fit().params['FDI_usd']:.3f}; "
      f"exact WLS {sm.WLS(b['I_cad'], Xc, weights=e**-2).fit().params['FDI']:.3f}; "
      f"unweighted {sm.OLS(b['I_cad'], Xc).fit().params['FDI']:.3f}; "
      f"+const {sm.OLS(b['I_cad'], sm.add_constant(Xc)).fit().params['FDI']:.3f}; "
      f"C$ OLS {sm.OLS(b['I_cad'], sm.add_constant(Xc.drop(columns='e'))).fit().params['FDI']:.3f}")

print("\nK. Capacity interaction aligned with the two-term timing (equation 11)")
for x in ["Y", "N"]:
    dd = prep(base, x=x)
    m = smf.ols(PRIMARY + " + S + FDI:S + FDI_l1:S", data=dd).fit(**HAC)
    j = m.wald_test("FDI:S = 0, FDI_l1:S = 0", scalar=True)
    print(f"  X={x}: eta0={m.params['FDI:S']: .4f} (p={fmt_p(m.pvalues['FDI:S'])}), eta1={m.params['FDI_l1:S']: .4f} "
          f"(p={fmt_p(m.pvalues['FDI_l1:S'])}), joint p={fmt_p(j.pvalue)}, BG={fmt_p(bg(m))}, n={int(m.nobs)}")
    s_est = dd.loc[m.model.data.row_labels, "S"]
    for q in (0.25, 0.5, 0.75):
        s = s_est.quantile(q)
        out = []
        for name, expr in [("contemp", f"FDI + {s:.6f}*FDI:S"), ("lagged", f"FDI_l1 + {s:.6f}*FDI_l1:S"),
                           ("sum", f"FDI + FDI_l1 + {s:.6f}*FDI:S + {s:.6f}*FDI_l1:S")]:
            t = m.t_test(f"{expr} = 0"); lo, hi = t.conf_int()[0]
            out.append(f"{name} {float(t.effect[0]): .3f} [{lo: .3f}, {hi: .3f}]")
        print(f"    S p{int(q*100)}={s: .2f}%:  " + ";  ".join(out))
    est_i = dd[["dI", "dX", "U", "FDI", "FDI_l1", "S", "y2001", "y2009", "y2015"]].dropna()

    def eta_row(label, mm):
        ci = mm.conf_int()
        ts = mm.t_test("FDI:S + FDI_l1:S = 0"); slo, shi = ts.conf_int()[0]
        print(f"    {label:<26} eta0={mm.params['FDI:S']: .3f} [{ci.loc['FDI:S', 0]: .3f}, {ci.loc['FDI:S', 1]: .3f}]  "
              f"eta1={mm.params['FDI_l1:S']: .3f} [{ci.loc['FDI_l1:S', 0]: .3f}, {ci.loc['FDI_l1:S', 1]: .3f}]  "
              f"joint p={fmt_p(mm.wald_test('FDI:S = 0, FDI_l1:S = 0', scalar=True).pvalue)}  "
              f"eta0+eta1={float(ts.effect[0]): .3f} [{slo: .3f}, {shi: .3f}] p={fmt_p(float(ts.pvalue))}")

    eta_row("baseline", m)
    for label, extra in [("+ 2009", " + y2009"), ("+ 2001, 2009", " + y2001 + y2009"),
                         ("+ 2001, 2009, 2015", " + y2001 + y2009 + y2015")]:
        eta_row(f"indicators {label}", smf.ols(PRIMARY + " + S + FDI:S + FDI_l1:S" + extra, data=dd).fit(**HAC))
    # omission: HAC on a gapped sequence is descriptive only (see Appendix B)
    eta_row("omit 2009 (descriptive)", smf.ols(PRIMARY + " + S + FDI:S + FDI_l1:S", data=est_i.drop(2009)).fit(**HAC))
    eta_row("omit 2001 (descriptive)", smf.ols(PRIMARY + " + S + FDI:S + FDI_l1:S", data=est_i.drop(2001)).fit(**HAC))
    r = smf.ols("dI ~ dX + S + FDI + FDI:S", data=dd).fit(**HAC)
    print(f"    restricted (contemporaneous only): eta={r.params['FDI:S']:.4f} p={fmt_p(r.pvalues['FDI:S'])}")
    u = smf.ols(PRIMARY + " + FDI:U + FDI_l1:U", data=dd).fit(**HAC)
    print(f"    nominal-U comparison: joint p={fmt_p(u.wald_test('FDI:U = 0, FDI_l1:U = 0', scalar=True).pvalue)}")

print("\nL. US$ comparison")
du = prep(base, "usd")
m = smf.ols("dI ~ dX + U + FDI + ECT", data=du).fit(**HAC); print(f"  US$ ECM, FDI_t only: {m.params['FDI']:.3f} (p={fmt_p(m.pvalues['FDI'])})")
show_two_term("US$ ECM, two-term", two_term(smf.ols(PRIMARY + " + ECT", data=du).fit(**HAC)))
show_two_term("US$ change eq, two-term", two_term(smf.ols(PRIMARY, data=du).fit(**HAC)))

# ---------------------------------------------------------------------------------------------
# Source checks that need downloads (World Bank API, Statistics Canada table). Opt in with --online.
import sys
if "--online" in sys.argv:
    import io, json, urllib.request, zipfile
    from statsmodels.tsa.filters.hp_filter import hpfilter

    print("\nM. World Bank conversion check, gross national expenditure (Section 5.1)")
    def wb(code):
        url = f"https://api.worldbank.org/v2/country/CAN/indicator/{code}?format=json&date=1981:2018&per_page=100"
        rows = json.load(urllib.request.urlopen(url, timeout=60))[1]
        return pd.Series({int(r["date"]): r["value"] for r in rows}).sort_index()
    lcu, usd = wb("NE.DAB.TOTL.CN"), wb("NE.DAB.TOTL.CD")
    print(f"  max |LCU/USD - archived fx| = {(lcu / usd - base['fx']).abs().max():.4f}")
    print(f"  max relative gap, archived Y_cad vs WB LCU = {((lcu / 1e9 - base['Y_cad']) / base['Y_cad']).abs().max():.4f}")

    print("\nN. HP-filter vintage and endpoint checks (Section 5.7)")
    raw = urllib.request.urlopen("https://www150.statcan.gc.ca/n1/tbl/csv/36100222-eng.zip", timeout=300).read()
    t = pd.read_csv(zipfile.ZipFile(io.BytesIO(raw)).open("36100222.csv"), low_memory=False)
    s = t[(t.GEO == "Canada") & (t.Prices == "Chained (2017) dollars") &
          (t.Estimates == "Gross domestic product at market prices") & (t.UOM == "Dollars")]
    rg = s.assign(year=s.REF_DATE.astype(int)).set_index("year")["VALUE"].dropna()
    gap = lambda end: 100 * (np.exp(hpfilter(np.log(rg.loc[:end]), lamb=100)[0]) - 1)
    full, g18 = gap(rg.index.max()), gap(2018)
    print(f"  real GDP vintage {rg.index.min()}-{rg.index.max()}; max |full - archived gap_pct| = "
          f"{(full.loc[1981:2018] - base['gap_pct']).abs().max():.3f} pp")
    dd = (g18 - full).loc[1981:2018]
    print(f"  filter ending 2018 vs full: corr {np.corrcoef(g18.loc[1981:2018], full.loc[1981:2018])[0,1]:.3f}, "
          f"max |diff| {dd.abs().max():.2f} pp in {dd.abs().idxmax()}")
    rt = pd.Series({y: gap(y).loc[y] for y in range(1990, 2019)})
    print(f"  one-sided vs full-sample gap, 1990-2018: corr {np.corrcoef(rt, full.loc[1990:2018])[0,1]:.3f}")

    print("\nO. Statistics Canada native-C$ FDI series (separate check; archived data unchanged)")
    def statcan(table):
        raw = urllib.request.urlopen(f"https://www150.statcan.gc.ca/n1/tbl/csv/{table}-eng.zip", timeout=300).read()
        return pd.read_csv(zipfile.ZipFile(io.BytesIO(raw)).open(f"{table}.csv"), low_memory=False)
    a = statcan("36100471")
    liab = (a[(a.GEO == "Canada") & (a["Financial account"] == "Direct investment liabilities")
              & (a["Countries or regions"] == "All countries")]
            .assign(year=lambda z: z.REF_DATE.astype(int)).set_index("year")["VALUE"] / 1000)
    q = statcan("36100442")
    q = q[(q["Asset liability and directional direct investment presentations"]
           == "Equals: Foreign direct investment in Canada (directional presentation)")
          & (q["Geographic region"] == "All countries")]
    q = q.assign(year=q.REF_DATE.str[:4].astype(int))
    nq = q.groupby("year").size()
    directional = (q.groupby("year")["VALUE"].sum() / 1000)[nq == 4]
    url = "https://api.worldbank.org/v2/country/CAN/indicator/{}?format=json&date=1981:2024&per_page=100"
    wbget = lambda c: pd.Series({int(r["date"]): r["value"] for r in json.load(urllib.request.urlopen(url.format(c), timeout=60))[1]}).sort_index()
    wb_cad = wbget("BX.KLT.DINV.CD.WD") * wbget("PA.NUS.FCRF") / 1e9
    for name, ser in [("current WB x FX", wb_cad), ("archived FDI_cad", base["FDI_cad"])]:
        d_ = (ser - liab).loc[1981:2018].dropna()
        print(f"  {name:<18} vs StatCan liabilities 1981-2018: corr {ser.loc[1981:2018].corr(liab.loc[1981:2018]):.5f}, "
              f"mean |diff| {d_.abs().mean():.3f}, max |diff| {d_.abs().max():.3f} in {d_.abs().idxmax()}")
    print(f"  directional series available {directional.index.min()}-{directional.index.max()} (complete years)")
    for yr in (2007, 2009, 2015, 2018, 2024):
        print(f"    {yr}: WBxFX {wb_cad.get(yr, np.nan):8.3f}  liabilities {liab.get(yr, np.nan):8.3f}  directional {directional.get(yr, np.nan):8.3f}")

    print("  primary equation (7), C$, X = Y, with alternative FDI series:")
    for label, ser, start in [("archived (baseline)", base["FDI_cad"], 1981), ("StatCan liabilities", liab, 1981),
                              ("archived, 1991-2018", base["FDI_cad"], 1990), ("StatCan directional", directional, 1990)]:
        alt = base.loc[start:2018].copy()
        alt["FDI_cad"] = ser.reindex(alt.index)
        for x in ["Y", "N"]:
            show_two_term(f"{label}, X={x}", two_term(smf.ols(PRIMARY, data=prep(alt, x=x)).fit(**HAC)))
