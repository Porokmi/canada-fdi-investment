# Project history and revision notes

## Origin and scope

This study began as a 2019 undergraduate project and was revisited in 2026 to strengthen empirical research skills and develop the research portfolio. The revised work reconstructs the data, uses Python rather than the original EViews workflow, tests time-series assumptions, and reassesses the economic interpretation. The [original 2019 paper](../archive/2019/Sambahamphe_FDI_Canada_2019.pdf) is archived unchanged.

The [Extended Working Paper](../paper/Sambahamphe_FDI_Canada_Extended_Working_Paper.pdf) is the latest full research draft. The [shorter revised paper](../paper/Sambahamphe_FDI_Canada.pdf) is retained as a concise version. The archive preserves the undergraduate submission as historical work rather than a current alternative estimate.

### What changed from the archived paper

The original identifies itself as an ECON 310-01 term paper from Fall 2019. It reports OLS and an AR(1) model estimated by ARMA maximum likelihood in EViews. Its AR(1) table reports an FDI coefficient of 0.136900 (p = 0.0243). The 2026 reconstruction uses different data and an iterative GLSAR estimator; it should not be described as an exact replication of that table.

Several original EViews estimation tables explicitly list **1981–2016 and 36 observations**, while parts of the narrative refer to 1981–2018. The revised main sample explicitly covers **1981–2018 and 38 observations**. This discrepancy is preserved and documented, not silently corrected in the archived file. The revised analysis also defines capacity slack differently and examines stationarity, cointegration, and currency sensitivity. The original's comparison of the FDI coefficient with one is replaced by a more cautious interpretation of conditional associations.

## Interpretation of the current results

- Business gross fixed capital formation includes foreign-owned firms. It is not a measure of investment by domestically owned firms alone.
- FDI is a financial-flow measure; its coefficient is not automatically a coefficient on new foreign-owned fixed investment. Comparing it with one does not establish crowding in or crowding out.
- Gross national expenditure includes investment. The investment-expenditure relationship includes an accounting component and is not an independently identified demand effect.
- FDI enters the baseline ECM in levels. Its coefficient describes a conditional association between the inflow level and the annual change in investment; it is not an elasticity, a causal effect, or the response to a change in FDI.
- Failure to reject a zero coefficient is not evidence that the economic effect is exactly zero. The cointegration test also does not establish a causal relationship.

## Supplementary checks run on the archived CSVs

Run `python src/specification_audit.py` after installing the repository requirements. Outputs are written to `tables/audit/` without overwriting the original paper tables.

The audit covers both currencies and both sample endpoints, reports ADF lag choices and observation counts, and compares a fixed set of dynamic specifications on common observations. All dynamic comparisons include 1983 onward (36 observations through 2018 and 42 through 2024). All extended-sample comparisons include a 2020 indicator. HAC standard errors use three lags and normal-reference inference (`use_t=False`). ADF levels include a constant and trend; differences include a constant; lag length is selected by AIC. Cointegration tests include a constant and use AIC lag selection.

### Main findings

1. For 1981-2018, the Canadian-dollar ADF tests reject a unit root for FDI (p < 0.001) and capacity slack (p = 0.010), but not for investment (p = 0.543) or expenditure (p = 0.970). These are specification-dependent test results, not definitive classifications. ADF chooses as many as eight lags in some tests, a substantial demand on a small annual sample.
2. Under the earlier audit’s default AIC settings, the investment-expenditure cointegration p-values are 0.002 for USD and 0.382 for CAD through 2018; through 2024 they are 0.358 and 0.291 respectively. Under those settings, CAD and extended-sample ECMs are exploratory comparisons. The Extended Working Paper also reports a capped BIC configuration that changes these conclusions; the evidence is sensitive to the tested settings.
3. The exchange-rate level does not reject a unit root at 5% in the main-sample trend specification (p = 0.075). Including that level in a change equation therefore needs additional justification. It does not mechanically undo time-varying currency conversion.
4. In the common-sample USD ECM, the FDI coefficient remains small and insignificant after adding lagged expenditure and investment changes. The two-lag Breusch-Godfrey test still rejects no serial correlation for the baseline and both lag variants. Adding lags is not a demonstrated solution to the diagnostic failure.
5. Replacing the FDI level with its first difference changes the question being estimated. The script reports this comparison explicitly; it should not be selected simply because its p-values or diagnostics look preferable. The common-sample CAD change equation with differenced FDI still rejects no serial correlation at 5%.

The supplementary common-sample models do not exactly reproduce the original 37-observation baseline because they deliberately hold the estimation years fixed when comparing lag structures. Their output is separate from the paper's reported results.

## Extended Working Paper November 2026

The new full draft and its editable Word version are in `paper/`. Its self-contained replication source is in [`extended/`](../extended/README.md), including data, figures, a manuscript source, and numerical outputs. Run `python extended/analysis.py` from the repository root after installing `extended/requirements.txt`.

The extension reports four explicit research questions and adds test-setting sensitivity, interaction marginal associations, HAC bandwidth comparisons, and leave-one-out coefficient influence. The main-sample CAD cointegration p-value changes from 0.382 under default AIC to 0.023 when the search is capped at three lags and BIC is used. The extended USD and CAD tests also change their conclusions. Both the search maximum and information criterion change together; this is not an isolated test of the criterion alone.

The extended USD change equation with differenced FDI yields about 0.146 (p = 0.031), while the corresponding CAD value is about 0.173 (p = 0.062). These measure associations with changes in inflows, not the inflow levels in the baseline ECM. The full draft reports them without treating one significant alternative as a preferred causal specification. Residual serial correlation and other limitations remain documented.

## Remaining research work

- Compare a parsimonious set of lag structures and deterministic terms using economic reasoning and residual diagnostics. Report the alternatives, rather than selecting for an FDI significance result.
- Examine real Canadian-dollar investment and expenditure using documented, compatible deflators. Current-price trends can reflect inflation as well as real activity; USD conversion adds exchange-rate movements.
- Assess sensitivity to large FDI episodes, structural instability, and the full-sample HP filter. The processed CSVs alone do not permit a faithful one-sided reconstruction of the original real-GDP filter.
- Clarify the implications of expenditure containing investment and distinguish conditioning on demand from estimating a total effect of FDI. Alternative demand measures require their own economic justification.
- Preserve causal restraint unless a credible identification strategy and suitable data are available. A negative coefficient, HAC errors, or cointegration alone does not identify displacement.
- Update the paper, notebook, tables, and figures together once a justified specification is settled. The shorter PDF retains the earlier prose revision and original tables. The Extended Working Paper incorporates and extends the diagnostics, with its own analysis and outputs.

## Reproducibility and assistance

The audit uses archived processed data, so it checks the estimation stage rather than independently verifying the source downloads or historical data vintage. Package versions can affect numerical details. AI assisted with this diagnostic script and documentation; author review and understanding remain necessary.
