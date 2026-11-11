# Foreign Direct Investment and Business Investment in Canada

Research papers, code, and archived data for *Foreign Direct Investment and Business Investment in Canada* (Porokmi Sambahamphe, revised November 2026). The main sample is 1981–2018, with an extension through 2024.

## Project history and current status

This project began as an undergraduate research paper in 2019. I revisited it in 2026 to strengthen my empirical research skills and develop it further for my research portfolio. The revision reconstructs the dataset, moves the analysis from EViews to Python, introduces unit-root and cointegration tests, and reassesses the interpretation of the original results.

The **Extended Working Paper** is the latest full research draft, with explicit research questions, a literature review, an economic framework, and expanded diagnostics. The **shorter paper** is a concise version with the same results. Both were revised in November 2026 after reviewer feedback: they now measure all series in Canadian dollars and let FDI enter with a one-year lag. The [original undergraduate paper](archive/2019/Sambahamphe_FDI_Canada_2019.pdf) is preserved in the [2019 archive](archive/2019/README.md). The findings are descriptive and sensitive to specification; this project does not identify a causal effect of FDI. See [the revision notes](docs/REVISION_NOTES.md) for what changed and the remaining methodological questions.

📄 **[Extended Working Paper — PDF](paper/Sambahamphe_FDI_Canada_Extended_Working_Paper.pdf)**

[Shorter paper](paper/Sambahamphe_FDI_Canada.pdf) · [Baseline notebook](FDI_Canada.ipynb) · [Extended analysis and results](extended/)

![FDI coefficient sum across specifications](figures/figure2_fdi_coefficients.png)

## The question

Foreign direct investment can finance new plants, equipment and technology, but a recorded inflow need not create an equivalent amount of fixed capital: foreign investors may acquire an existing firm or provide financing that substitutes for funds available elsewhere. Whether FDI adds to business investment (crowding in) or displaces it (crowding out) is therefore an empirical question. I examine it for Canada over 1981–2018, revisiting Van Loo (1977), who reported an FDI coefficient of about 1.40, and my original undergraduate regression, which assessed complementarity by comparing the FDI coefficient with one. The revision reconsiders whether that interpretation is justified.

## What I found

- **Canadian dollars are the primary unit.** Converting to US dollars at a moving exchange rate adds a revaluation component to every annual change. In 2015, investment fell by about C$15 billion, but its US-dollar value fell by US$62 billion, US$51 billion of which was exchange-rate revaluation.
- **Negative conditional association, mainly with a one-year lag.** In a change equation with current and lagged FDI, the coefficient sum is −0.130 (95% interval −0.188 to −0.073). It is negative in every Canadian-dollar specification examined and robust to Statistics Canada's own FDI series, single-year omissions and extra short-run dynamics.
- **Sensitive to how trends and expenditure are modelled.** With a linear trend and total expenditure as the control, the sum is −0.050 and not significant. The trend-free baseline is a presentation choice, not a specification the data show to be superior.
- **Currency explains the difference from the earlier US-dollar results.** An exact algebraic bridge attributes most of the gap to revaluation introduced by differencing in US dollars, in every one of the 120 orders of the adjustments.
- **Capacity slack shifts the timing of the association, not its combined size,** and that timing evidence is sensitive to the 2001 and 2009 downturns.
- **No identified displacement.** These are conditional associations. Acquisition-driven inflows and inflows that peak late in investment upswings could both produce the pattern, and aggregate data cannot tell them apart.

### Earlier versions

The October and 1 November 2026 versions measured everything in US dollars and entered only current FDI. There the FDI coefficients were positive but insignificant (OLS 0.124, AR(1) 0.053, error-correction model 0.027), and Canadian-dollar change equations gave about −0.107. The archived data are unchanged; the earlier PDFs remain in the git history, and the 1 November extended replication package is kept in [`extended/`](extended/README.md).

## Methods

| Step | Method | Notebook section | Extended paper |
|---|---|---|---|
| Capacity slack | HP filter (λ = 100) on log real GDP; slack in C$ and as % of potential | 2 | 4.3, 5.7 |
| Stationarity | ADF tests with deterministic terms matched to each variable's role | 4 (Table 1) | 5.3, 6.1 |
| Long-run link | Engle–Granger cointegration, two lag-selection settings, two expenditure measures | 5 | 5.5, 6.1 |
| Baseline model | C$ change equation with current and lagged FDI; Wald tests of timing restrictions; HAC errors | 6 (Table 2) | 5.5, 6.2 |
| Sensitivity | Trend, expenditure excl. investment, ECM, 1981–2024, extra dynamics, Statistics Canada FDI series | 7 (Table 3) | 7.1, 7.3 |
| Currency bridge | Exact US$→C$ translation; Shapley attribution over all 120 adjustment orders | 8 | 5.6, 7.2 |
| Capacity interaction | Timing-aligned interactions; joint and coefficient-sum tests | 9 | 5.7, 7.4 |
| Exploratory checks | Downturn-year indicators (2001, 2009, 2015) | 9 | Appendix D |

## Data

| Variable | Source |
|---|---|
| Business gross fixed capital formation (I), nominal and real GDP | Statistics Canada, [Table 36-10-0222-01](https://doi.org/10.25318/3610022201-eng) |
| Gross national expenditure (Y) | World Bank WDI, `NE.DAB.TOTL.CD` (checked against `NE.DAB.TOTL.CN`) |
| FDI net inflows | World Bank WDI, `BX.KLT.DINV.CD.WD` |
| Exchange rate (CAD per USD) | World Bank WDI, `PA.NUS.FCRF` |
| FDI source checks (current releases) | Statistics Canada Tables 36-10-0471-01, 36-10-0442-01, 36-10-0025-01 |

The processed datasets used in the papers are in [`data/`](data) and are frozen for reproducibility. Values are in billions (US$ and C$ versions of each series). See [the data notes](data/README.md) for variable definitions and reconstruction limits.

*Source: Statistics Canada. Reproduced and distributed on an "as is" basis with the permission of Statistics Canada, under the [Statistics Canada Open Licence](https://www.statcan.gc.ca/en/terms-conditions/open-licence). World Bank data used under [CC BY 4.0](https://datacatalog.worldbank.org/public-licenses).*

## Reproduce

1. Clone or download the **whole repository**, including `data/`, and open a terminal in its root folder.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Open `FDI_Canada.ipynb` in Jupyter and run all cells. If Jupyter is not installed, use `python -m pip install notebook` and `python -m notebook`.
4. Keep `REBUILD_DATA = False` to reproduce the reported estimates from the saved CSVs. Set it to `True` only to retrieve newer source data; revisions can change the results. Set `FETCH_SOURCE_CHECKS = False` to skip the Statistics Canada FDI comparisons, which download current releases.

For Google Colab, first clone the repository and switch to its folder in a setup cell, then run the notebook there:

```python
!git clone https://github.com/Porokmi/canada-fdi-investment.git
%cd canada-fdi-investment
!pip install -r requirements.txt
```

The notebook writes figures to `figures/` and tables (CSV, and PNG versions used in the shorter paper) to `tables/`.

Supplementary specification checks from the earlier US-dollar revision: `python src/specification_audit.py`. These use the archived CSVs and write separate outputs to `tables/audit/`; they do not overwrite the paper's tables.

### Reproduce the Extended Working Paper

From the repository root:

```sh
python extended/paper_outputs.py --online   # every table and figure -> extended/output/
python extended/checks.py --online          # full diagnostics, including the currency bridge
```

Both scripts read only the archived CSVs. `--online` adds the comparisons with current World Bank and Statistics Canada releases; without it, those rows are skipped. The results were produced with statsmodels 0.15.0 and pandas 3.1.0. The 1 November 2026 version of the extended analysis (`extended/analysis.py`, with its pinned `extended/requirements.txt`) is kept for reference; see [`extended/README.md`](extended/README.md).

## Repository

| Location | Contents |
|---|---|
| [Extended Working Paper](paper/Sambahamphe_FDI_Canada_Extended_Working_Paper.pdf) | Latest full draft in PDF format (revised November 2026) |
| [Shorter paper](paper/Sambahamphe_FDI_Canada.pdf) | Concise revised paper (revised November 2026) |
| [Notebook](FDI_Canada.ipynb) | Shorter paper's analysis and exports (C$) |
| [Extended analysis](extended/) | Scripts, outputs, manuscript build files and revision notes for the Extended Working Paper; the 1 November package |
| [Paper source](paper/source/) | Source text and script that assemble the revised shorter paper |
| [Original paper](archive/2019/) | Unchanged 2019 undergraduate paper and archive notes |
| [Data](data/) | Saved datasets and variable definitions |
| [Figures](figures/) | Charts used in the shorter paper |
| [Tables](tables/) | Shorter paper's tables and supplementary audit outputs |
| [Audit script](src/specification_audit.py) | Separate specification checks from the earlier revision |
| [Revision notes](docs/REVISION_NOTES.md) | Changes, diagnostics, and remaining research questions |
| [Requirements](requirements.txt) | Python dependencies |

## AI disclosure

AI assistance was used for coding, econometric discussion, source discovery, drafting, editing, and document preparation. The research question and the original undergraduate project are the author's. The calculations in this package were executed on the archived data, but execution and internal consistency do not independently validate source measurement or causal assumptions. The author remains responsible for understanding the analysis, checking the cited sources, and deciding how the draft is used.
