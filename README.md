# Does FDI Stimulate Business Investment in Canada? (1981–2018)

Code and archived data for *Foreign Direct Investment and Business Investment in Canada* (Porokmi Sambahamphe, revised 2026).

## Project history and current status

This project began as an undergraduate research paper in 2019. I revisited it in 2026 to strengthen my empirical research skills and develop it further for my research portfolio. The revision reconstructs the dataset, moves the analysis from EViews to Python, introduces unit-root and cointegration tests, and reassesses the interpretation of the original results.

The linked paper is the current revised draft. The [original undergraduate paper](archive/2019/Sambahamphe_FDI_Canada_2019.pdf) is preserved in the [2019 archive](archive/2019/README.md). The findings are descriptive and sensitive to specification; this project does not identify a causal effect of FDI. See [the revision notes](docs/REVISION_NOTES.md) for the remaining methodological questions and supplementary checks.

📄 **[Read the paper](paper/Sambahamphe_FDI_Canada.pdf)** · 📓 **[Open the notebook](FDI_Canada.ipynb)**

![FDI coefficient across specifications](figures/figure2_fdi_coefficients.png)

## The question

Foreign direct investment can finance new plants, equipment and technology, but a recorded inflow need not create an equivalent amount of fixed capital: foreign investors may acquire an existing firm or provide financing that substitutes for funds available elsewhere. Whether FDI adds to business investment (crowding in) or displaces it (crowding out) is therefore an empirical question. I examine it for Canada over 1981–2018, revisiting Van Loo (1977), who reported an FDI coefficient of about 1.40, and my original undergraduate regression, which assessed complementarity by comparing the FDI coefficient with one. The revision reconsiders whether that interpretation is justified.

## What I found

- **No significant FDI association in the main US-dollar models:** OLS 0.124 (p = 0.156), AR(1) 0.053 (p = 0.405) and the error-correction model 0.027 (HAC p = 0.615).
- **The main US-dollar sample supports cointegration between investment and expenditure** (Engle–Granger p = 0.002): the estimated adjustment coefficient corresponds to about 37% of the previous year's deviation being corrected within a year, conditional on the model (error-correction term −0.369, p = 0.019).
- **The sign depends on currency:** Canadian-dollar change equations give a negative association of about −0.107 to −0.108 (p < 0.001), even with an exchange-rate control. Currency conversion behaves as a specification change, not a simple rescaling.
- **No robust evidence of a positive FDI association; the estimates do not establish a causal increase or decrease in investment.** FDI measures financial inflows, which can include acquisitions of existing assets, and the main ECM retains residual serial correlation (Breusch–Godfrey p = 0.001).

## Methods

| Step | Method | Notebook section |
|---|---|---|
| Capacity slack | HP filter (λ = 100) on log real GDP; U = potential − actual | 2 |
| Stationarity | Augmented Dickey–Fuller (levels with trend, differences) | 4 (Table 1) |
| Levels model | OLS, then AR(1) errors via iterative GLSAR | 5 |
| Long-run link | Engle–Granger cointegration of investment and expenditure | 6 |
| Short-run model | Error-correction model, Newey–West (HAC) standard errors | 6 (Table 2) |
| Diagnostics | Breusch–Godfrey serial-correlation test | 7 |
| Sensitivity checks | C$ units, 1981–2024 sample with 2020 indicator, FDI × U interaction, change equations with and without the exchange-rate level | 8 (Table 3) |

## Data

| Variable | Source |
|---|---|
| Business gross fixed capital formation (I), nominal and real GDP | Statistics Canada, [Table 36-10-0222-01](https://doi.org/10.25318/3610022201-eng) |
| Gross national expenditure (Y) | World Bank WDI, `NE.DAB.TOTL.CD` |
| FDI net inflows | World Bank WDI, `BX.KLT.DINV.CD.WD` |
| Exchange rate (CAD per USD) | World Bank WDI, `PA.NUS.FCRF` |

The processed datasets used in the paper are in [`data/`](data). Values are in billions (US$ and C$ versions of each series).

*Source: Statistics Canada, Table 36-10-0222-01. Reproduced and distributed on an "as is" basis with the permission of Statistics Canada, under the [Statistics Canada Open Licence](https://www.statcan.gc.ca/en/terms-conditions/open-licence). World Bank data used under [CC BY 4.0](https://datacatalog.worldbank.org/public-licenses).*

## Reproduce

1. Clone or download the **whole repository**, including `data/`, and open a terminal in its root folder.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Open `FDI_Canada.ipynb` in Jupyter and run all cells. If Jupyter is not installed, use `python -m pip install notebook` and `python -m notebook`.
4. Keep `REBUILD_DATA = False` to reproduce the reported estimates from the saved CSVs. Set it to `True` only to retrieve newer source data; revisions can change the results.

For Google Colab, first clone the repository and switch to its folder in a setup cell, then run the notebook there:

```python
!git clone https://github.com/Porokmi/canada-fdi-investment.git
%cd canada-fdi-investment
!pip install -r requirements.txt
```

The notebook writes figures to `figures/` and tables to `tables/`. See [the data notes](data/README.md) for variable definitions and reconstruction limits.

Supplementary specification checks: `python src/specification_audit.py`. These use the archived CSVs and write separate outputs to `tables/audit/`; they do not overwrite the paper's original tables. Models within each sample/currency comparison use common observations, so their coefficients need not match the paper's 37-observation baseline.

## Repository

| Location | Contents |
|---|---|
| [Current paper](paper/Sambahamphe_FDI_Canada.pdf) | Revised research paper |
| [Notebook](FDI_Canada.ipynb) | Main analysis and exports |
| [Original paper](archive/2019/) | Unchanged 2019 undergraduate paper and archive notes |
| [Data](data/) | Saved datasets and variable definitions |
| [Figures](figures/) | Charts used in the analysis |
| [Tables](tables/) | Main estimates and supplementary audit outputs |
| [Audit script](src/specification_audit.py) | Separate specification checks |
| [Revision notes](docs/REVISION_NOTES.md) | Changes, diagnostics, and remaining research questions |
| [Requirements](requirements.txt) | Python dependencies |

## AI assistance

The research question and original 2019 paper are my own. In revising the project, I used Claude and ChatGPT for econometric discussion, code development, data-processing and plotting routines, draft review and editing, and repository organization. AI assistance also supported the supplementary diagnostic script. The initial repository documentation records my role in specification choices, running the notebook models, and interpreting the results. I remain responsible for reviewing the code, understanding the methods, and assessing the conclusions.
