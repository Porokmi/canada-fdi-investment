"""Supplementary checks on the archived data; does not overwrite paper outputs.

Run from any directory: python src/specification_audit.py
These are descriptive sensitivity checks, not causal estimates or model selection.
"""
from pathlib import Path
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller, coint
from statsmodels.stats.diagnostic import acorr_breusch_godfrey

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tables' / 'audit'

def run():
    OUT.mkdir(parents=True, exist_ok=True)
    adf_rows, coint_rows, model_rows = [], [], []
    for end in (2018, 2024):
        raw = pd.read_csv(ROOT / 'data' / f'fdi_data_1981_{end}.csv', index_col='year')
        for unit in ('usd', 'cad'):
            d = pd.DataFrame({v: raw[f'{v}_{unit}'] for v in ('I', 'Y', 'U', 'FDI')})
            d['fx'] = raw['fx']
            d['covid'] = (d.index == 2020).astype(int)
            assert d.index.is_unique and d.index.is_monotonic_increasing
            assert d.notna().all().all()
            for v in ('I', 'Y', 'U', 'FDI', 'fx'):
                for transform, reg in [('level', 'ct'), ('difference', 'c')]:
                    s = d[v] if transform == 'level' else d[v].diff().dropna()
                    stat, p, lag, n, *_ = adfuller(s, regression=reg, autolag='AIC')
                    adf_rows.append(dict(end=end, currency=unit, variable=v, transform=transform,
                                         deterministic=reg, statistic=stat, p=p, lags=lag, n=n))
            stat, p, _ = coint(d['I'], d['Y'], trend='c', autolag='aic')
            coint_rows.append(dict(end=end, currency=unit, statistic=stat, p=p))
            d['ECT'] = smf.ols('I ~ Y', data=d).fit().resid.shift(1)
            for v in ('I', 'Y', 'FDI', 'fx'):
                d['d'+v] = d[v].diff()
                d['d'+v+'_lag'] = d['d'+v].shift(1)
            specs = {
                'ECM baseline': 'dI ~ dY + U + FDI + ECT',
                'ECM + lagged dY': 'dI ~ dY + dY_lag + U + FDI + ECT',
                'ECM + lagged dI and dY': 'dI ~ dY + dY_lag + dI_lag + U + FDI + ECT',
                'Change equation, FDI in levels': 'dI ~ dY + U + FDI',
                'Change equation + FX level': 'dI ~ dY + U + FDI + fx',
                'Change equation, differenced FDI': 'dI ~ dY + U + dFDI',
            }
            # Same observations within each sample/currency comparison.
            common = d.dropna()
            for label, formula in specs.items():
                if end == 2024:
                    formula += ' + covid'
                fit = smf.ols(formula, data=common).fit()
                hac = fit.get_robustcov_results(cov_type='HAC', maxlags=3, use_t=False)
                j = fit.model.exog_names.index('dFDI' if 'dFDI' in fit.params.index else 'FDI')
                lm, lm_p, _, _ = acorr_breusch_godfrey(fit, nlags=2)
                lo, hi = hac.conf_int()[j]
                model_rows.append(dict(end=end, currency=unit, specification=label,
                    formula=formula, n=int(fit.nobs), fdi_regressor=fit.model.exog_names[j],
                    fdi_coefficient=float(hac.params[j]), hac_se=float(hac.bse[j]),
                    hac_p=float(hac.pvalues[j]), ci_low=float(lo), ci_high=float(hi),
                    bg_lm=float(lm), bg_p=float(lm_p)))
    for filename, rows in [('stationarity.csv', adf_rows), ('cointegration.csv', coint_rows),
                           ('model_sensitivity.csv', model_rows)]:
        pd.DataFrame(rows).to_csv(OUT / filename, index=False)
    print(pd.DataFrame(coint_rows).to_string(index=False))
    print(pd.DataFrame(adf_rows).query("end == 2018 and transform == 'level'")[['currency','variable','p','lags']].to_string(index=False))
    print(pd.DataFrame(model_rows).query('end == 2018')[['currency','specification','n','fdi_coefficient','hac_p','bg_p']].to_string(index=False))

if __name__ == '__main__':
    run()
