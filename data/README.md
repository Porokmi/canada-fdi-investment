# Data notes

The saved CSVs are processed inputs used by the analysis notebook. They preserve the dataset used for the reported estimates; they are not raw source downloads. The original source retrieval date was not recorded in this repository.

| File | Coverage | Rows |
|---|---|---:|
| `fdi_data_1981_2018.csv` | Main annual sample, 1981–2018 | 38 |
| `fdi_data_1981_2024.csv` | Extended annual sample, 1981–2024 | 44 |

| Column | Definition | Units |
|---|---|---|
| `year` | Calendar year | Year |
| `fx` | Annual average exchange rate | CAD per USD |
| `gap_pct` | HP-based actual output relative to estimated potential, minus one | Percent of potential |
| `I_usd`, `I_cad` | Business gross fixed capital formation | Current-price billions, indicated currency |
| `Y_usd`, `Y_cad` | Gross national expenditure | Current-price billions, indicated currency |
| `U_usd`, `U_cad` | Estimated potential output minus actual output, valued at the nominal GDP price scale | Current-price billions, indicated currency |
| `FDI_usd`, `FDI_cad` | Foreign direct investment, net inflows | Current-price billions, indicated currency |

Positive `gap_pct` denotes output above estimated potential; positive `U` denotes output below estimated potential. These signs are intentionally opposite.

Business investment includes foreign-owned firms. FDI measures financial flows, not exclusively new fixed capital formation. Expenditure includes investment. These definitions constrain the interpretation of coefficients.

## Sources and reconstruction

Business investment and nominal/real GDP come from Statistics Canada Table 36-10-0222-01. Gross national expenditure, FDI net inflows, and the exchange rate use World Bank WDI codes `NE.DAB.TOTL.CD`, `BX.KLT.DINV.CD.WD`, and `PA.NUS.FCRF`.

The notebook constructs potential output from an HP filter (lambda = 100) on the full available log real-GDP series. The archived CSVs do not contain that full real-GDP input, so the filtering stage cannot be independently reconstructed from these files alone. Setting `REBUILD_DATA = True` downloads current source data and may produce different values because of source revisions, changed series labels, and the full-series filter.

Run the notebook with `REBUILD_DATA = False` to use the saved data. Supplementary audit outputs in `tables/audit/` are distinct from the paper's main tables and use common samples for dynamic comparisons.
