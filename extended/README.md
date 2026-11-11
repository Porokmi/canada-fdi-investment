# Canada FDI extended working paper replication package

This folder accompanies the Extended Working Paper by Porokmi Sambahamphe. It extends the shorter paper with explicit research questions, a literature discussion, an economic framework, and additional diagnostics. The analysis estimates conditional associations rather than causal effects.

## Current version (revised 11 November 2026)

The revised paper measures all series in Canadian dollars and uses a change equation with current and lagged FDI as its baseline. From the repository root:

```sh
python extended/paper_outputs.py --online   # every table and figure in the paper -> output/
python extended/checks.py --online          # full diagnostics printout
```

| File | Contents |
|---|---|
| `paper_outputs.py` | Builds every table (`output/paper_tables.json`) and figure (`output/figures/`) in the revised paper |
| `checks.py` | Full diagnostics, including the currency bridge, interaction tests and source checks |
| `output/bridge_combinations.csv` | All 80 fitted currency-bridge models, with design-matrix rank and condition number |
| `manuscript/` | Source text and script that assemble the revised .docx from the original Word file |
| `revision_notes.md` | Revised motivation and methodology, with the changelog of the review |

Both scripts read only the archived CSVs in `../data/`. `--online` adds comparisons with current World Bank and Statistics Canada releases; without it, those rows are skipped.

## Version of 1 November 2026 (kept for reference)

The files below reproduce the first version of the Extended Working Paper, which used US dollars as the primary unit. Its PDF is in the git history; its conclusions are superseded by the revision above.

## Reproduce the analysis (1 November version)

Use Python 3.12 in a virtual environment. From this folder:

```sh
python -m pip install -r requirements.txt
python analysis.py
```

The script reads only `data/` and writes tables to `results/` and charts to `figures/`. It does not download new data. `results/environment.json` records versions and input hashes; `results/run_summary.txt` records the executed run used for the paper. The manuscript is in `manuscript.md`; its table and figure markers refer to the generated outputs. Word/PDF formatting is delivered separately.

## Data and interpretation

The processed annual datasets cover 1981–2018 and 1981–2024. They are the archived datasets from the project repository, not freshly downloaded source values. The original source retrieval date and complete real-GDP filtering inputs are not recorded in these CSVs. This package reproduces the estimation stage, not an independent historical reconstruction of the complete source-data pipeline.

Statistics Canada Table 36-10-0222-01 supplies business investment and the GDP inputs used in the original construction. World Bank WDI series are NE.DAB.TOTL.CD, BX.KLT.DINV.CD.WD, and PA.NUS.FCRF. Amounts with `_usd` and `_cad` suffixes are current-price billions. `fx` is CAD per USD. `U` is positive below potential; `gap_pct` is positive above potential.

Data-source attribution and terms: Statistics Canada, https://doi.org/10.25318/3610022201-eng and https://www.statcan.gc.ca/en/terms-conditions/open-licence; World Bank, https://datacatalog.worldbank.org/public-licenses. Derived files remain subject to relevant source terms.

## Diagnostic conventions

The main model uses all available observations. The common-sample lag comparisons begin in 1983. The alternative test setting jointly changes the lag-search maximum to three and the selection criterion to BIC. Change equations with FDI levels and changes estimate different parameters. HAC inference uses three lags unless otherwise labeled and a normal reference distribution. The leave-one-out output reports coefficients only, with derived variables held fixed; inferential p-values are not reported on these gapped deletion samples.

Key limitations include endogeneity, nominal scaling, ownership and entry-mode mismatch, estimated capacity slack, residual serial correlation, small samples, and cointegration sensitivity. The script reports fixed comparisons rather than choosing a model by its FDI p-value.

AI assisted with code, analysis discussion, and writing. Author review and understanding remain necessary. The repository's original 2019 PDF is preserved separately and is not included in this package.
