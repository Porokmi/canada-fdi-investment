# Draft: revised motivation and methodology (v4, author-edited)

*Extended Working Paper, "Foreign Direct Investment and Business Investment in Canada." This is the author's edited draft of 11 November 2026, with the remaining [CHECK] markers resolved. Every regression number is reproduced by `drafts/revision_checks.py` from the archived CSVs (`python drafts/revision_checks.py`). The source comparisons in Sections 5.1 and 5.7 and the alternative-FDI regressions need `--online`, which downloads current World Bank and Statistics Canada data.*

## Changelog: changes to the author's v4 text

| # | Where | Item | Resolution |
|---|---|---|---|
| 1 | §1 finding 3; §5.7 | Test of η₀ + η₁ = 0 "awaits" | Run. η₀ + η₁ = −0.060 [−0.136, 0.015], p = 0.116 (Y); −0.066 [−0.174, 0.042], p = 0.231 (N). Finding 3 and the §5.7 interpretation now state the result. |
| 2 | §5.7 | Report interaction coefficients and intervals for the indicator and omission checks | Added to the Notes table. |
| 3 | §5.6 | [CHECK] retain 32 outputs; verify full rank | All 80 fitted combinations (32 + 32 + 16 across the three bridges) are full rank, with a maximum condition number of 1,371. Saved to `drafts/output/bridge_combinations.csv`. |
| 4 | §5.1; verification note | "A robustness check using Statistics Canada's native-C$ liability series … has not been run" | Run, together with the directional check. Results added. |
| 5 | §5.6 ¶1 | "for FDI the source conversion cannot be checked from World Bank data alone" | Updated to cite the Statistics Canada comparison. |
| 6 | Verification note | Comparison statistics | Independently reproduced: corr 0.99986, mean gap 0.242, max gap 3.239 in 2007, and all five table rows. |
| 7 | Notes header | "script and archived CSVs were not supplied and have not been independently rerun here" | Replaced. The script was rerun on the archived CSVs on 11 November 2026. |
| 8 | §5.8 table | — | Row added for the alternative FDI series. |

**No markers remain.** The open decisions are:
- the linear-trend choice (the draft keeps the trend-free baseline and reports the trend version prominently);
- whether the exploratory downturn indicators stay in the main text or move to an appendix.

---

## 1 Introduction

The relationship between foreign direct investment and domestic capital formation matters for Canadian investment policy. Under the Investment Canada Act, acquisitions subject to net-benefit review are assessed for their likely benefit to Canada. The relevant factors include effects on economic activity, employment and productivity (Investment Canada Act, ss. 20–21). At the same time, weak business investment has been a recurring concern in Canadian economic policy discussion. Rogers (2024), for example, identifies persistent weakness in capital spending and investment per worker as a central productivity concern. Whether foreign direct investment adds to business capital formation is therefore not only an academic question: it bears on how inflows are assessed when they arrive.

The difficulty is that a recorded FDI inflow and an addition to the capital stock are different economic objects. A new foreign-owned plant is fixed investment. The purchase of an existing firm is an international financial transaction that may add little to fixed assets in the year it occurs. The Canadian data make the gap visible. In the archived World Bank-based series, annual FDI inflows peaked at about C$129 billion in 2007, equivalent to about 42 percent of business gross fixed capital formation that year (author's calculations). Statistics Canada's contemporary account identifies cross-border mergers and acquisitions as the main driver of that year's inward FDI, with fourth-quarter flows concentrated in energy and metallic minerals (Statistics Canada 2008). The historical release supports the acquisition context; it is not the source of the C$129 billion estimate, which uses a different data vintage and series construction. They then fell by more than four-fifths within two years. Business investment moved far less (Figure 1). An aggregate regression of investment on FDI must contend with this mismatch between what is measured and what is meant.

This paper reconstructs and extends my undergraduate study, a Fall 2019 term paper. It regressed business investment on expenditure, capacity slack and FDI, all measured in US dollars, found a positive FDI coefficient, and read it as evidence that foreign and domestic investment are complements. Reconstructing the data produces a sharper puzzle. In US dollars, the FDI coefficient in an equation for investment changes is essentially zero (0.001). In Canadian dollars, using the same underlying data, it is −0.107 and highly significant. The economy, sample and regression form are the same, but time-varying currency conversion changes the movements being modelled.

Canadian dollars are the primary unit because the question concerns nominal business capital formation within Canada. Converting these series into US dollars at a changing exchange rate introduces a revaluation component into annual changes. A decomposition of the archived series illustrates its potential importance. In 2015, investment declined by about C$15 billion, while its US-dollar value declined by approximately US$62 billion. About US$51 billion of that decline is exchange-rate revaluation, as the Canadian dollar depreciated from 1.105 to 1.279 per US dollar. This component does not itself represent additional or cancelled investment spending, although exchange rates may also influence investment decisions. Canadian-dollar measurement removes this conversion component; it does not remove inflation. The analysis therefore concerns changes in nominal investment, rather than changes in the volume of capital formation.

I study the relationship using 38 annual observations for 1981–2018, with an extension through 2024. The outcome is business gross fixed capital formation located in Canada, including investment by foreign-owned firms. The explanatory variable of interest is FDI net inflows, conditioned on aggregate expenditure and an estimated capacity-slack measure.

The reported estimates support three findings.

1. **The baseline Canadian-dollar specification gives a negative conditional FDI association, with sensitivity to specification.**
   - The sum of the contemporaneous and lagged coefficients is −0.130, with a 95 percent interval of [−0.188, −0.073].
   - It remains negative when expenditure excludes business investment (−0.135), when selected downturn-year indicators are added, when individual observations are omitted, and when lagged investment and expenditure changes are added.
   - It also remains negative when the World Bank FDI series is replaced by Statistics Canada's native-C$ direct investment liabilities (−0.131), or by its directional inward-FDI series over 1991–2018 (−0.146).
   - However, adding a trend with Y as the expenditure control reduces the sum to −0.050, with an interval including zero. Some ECM and extended-sample estimates are also imprecise.
   - The lagged coefficient is larger in magnitude than the contemporaneous coefficient, but the baseline test of its exclusion gives p = 0.089. Evidence about the timing is therefore weaker than evidence against a zero coefficient sum in that specification.
2. **Currency measurement materially changes the magnitude of the estimated association.** The reported exact bridge moves the baseline FDI coefficient sum from −0.025 in US dollars to −0.130 in Canadian dollars. Averaging over all 120 orders of the five specified adjustments, replacing exchange-rate-revalued changes with Canadian-dollar changes contributes −0.096 of the total movement of approximately −0.105. Its contribution ranges from −0.108 to −0.084 across orders. The remaining adjustments have smaller average contributions. Within this specified decomposition, revaluation in the differenced variables therefore accounts for most of the currency-related movement. This is an accounting attribution, conditional on the adjustments and their grouping, rather than a causal explanation or a decomposition of sampling uncertainty.
3. **Capacity conditions are associated with changes in the estimated timing pattern, but not with a detectable change in the combined association, and the evidence is sensitive to influential years.**
   - In the timing-aligned model, the interaction terms are jointly significant with either expenditure control (p < 0.001), with a positive contemporaneous interaction and a negative lagged interaction. Greater current slack is therefore associated with a more positive contemporaneous FDI coefficient and a more negative lagged coefficient.
   - Adding indicators for 2001 and 2009 weakens the joint evidence, with p = 0.110 using Y and p = 0.035 using N.
   - The sum of the two interaction coefficients, which measures whether slack changes the combined association, is −0.060 with Y (95 percent interval [−0.136, 0.015], p = 0.116) and −0.066 with N (p = 0.231).
   - These results suggest an exploratory change in the timing pattern. They provide no evidence that slack strengthens or weakens the combined FDI association.

These results describe conditional associations. They do not establish that foreign investment displaces domestic investment. Acquisitions followed by changes in capital spending and inflows concentrated late in an investment upswing are possible explanations for a negative association, but the aggregate data cannot distinguish these mechanisms. Transaction- and ownership-level data would be needed to investigate them.

### 1.1 Research questions

**RQ1.** Are annual FDI net inflows associated with annual changes in nominal business investment in Canada after conditioning on expenditure and estimated capacity slack? I report contemporaneous and lagged coefficients and their sum, and test the timing restrictions implicit in earlier specifications.

**RQ2.** Is there evidence of a cointegrating relationship between business investment and expenditure? Is that conclusion stable across currency, sample endpoint, lag-selection settings, and the definition of expenditure? The evidence informs the use of error-correction specifications, alongside integration-order and dynamic-specification checks.

**RQ3.** Does the conditional FDI association depend on available capacity?

**RQ4.** Why do the Canadian-dollar and US-dollar specifications produce different estimates? I answer this through an exact bridge between the two specifications rather than by listing alternative estimates.

### 1.2 Scope

The study is descriptive. It estimates conditional associations and introduces no instrument, policy discontinuity or other source of plausibly exogenous variation in inflows. Three features of the data limit what any coefficient here can mean.

- FDI is a balance-of-payments financial flow, not foreign-owned fixed investment.
- The investment series does not separate domestic from foreign owners.
- Annual aggregate data cannot distinguish greenfield entry from acquisitions.

A negative coefficient is therefore not evidence that foreign investment displaces domestic investment, and a coefficient below one is not evidence of displacement either (Section 3.2).

The project's contribution is a transparent reconstruction of an earlier study, with the specification choices that drive its conclusions isolated and tested rather than catalogued. The undergraduate paper and its EViews output are preserved separately (Appendix C).

---

## 3.3 Conditional associations and the composition of expenditure

Including expenditure changes the question in two ways.

**Behavioural.** If FDI raises investment partly by expanding demand, conditioning on expenditure removes part of that pathway. If expected growth both attracts foreign investors and raises expenditure, the control removes one source of confounding. A regression coefficient cannot distinguish these, and the control does not make the remaining FDI variation exogenous.

**Accounting.** Gross national expenditure contains business investment: Y = I + N, where N is all other expenditure (consumption, government spending, residential and non-business investment). Holding Y fixed while I varies therefore implies an equal and opposite movement in N. The conditional FDI coefficient in a regression that controls for Y describes how FDI covaries with the composition of expenditure between business investment and everything else, not with business investment holding demand fixed.

The same structure applies to any long-run regression of I on Y (Section 5.5). Any cointegrating relation must be interpreted with this accounting overlap in mind. It does not automatically establish a stable investment share or an independent demand relationship. Moreover, replacing Y with N = Y − I is an invertible linear transformation of the pair (I, Y). It therefore does not provide independent population evidence of cointegration, although finite-sample residual-based test results may differ.

To make the estimand explicit, I re-estimate the main specifications with expenditure net of business investment, N = Y − I, in place of Y, on identical observations. Netting out I does not resolve simultaneity, since N and I are jointly determined. It does show whether the FDI results depend on conditioning on an aggregate that contains the outcome. Both series are available in each currency in the archived data, so the comparison requires no new sources.

---

## 5 Empirical strategy

The analysis uses a baseline Canadian-dollar change equation (Section 5.5) and reports alternative specifications addressing currency measurement, deterministic terms, expenditure composition and dynamics. These specifications were developed during the revision; they are not described as prospectively pre-specified. The selected downturn-year indicators were added after inspecting the data and are treated as exploratory. Model choices are justified by the research question and statistical assumptions, rather than by the significance of FDI.

### 5.1 Currency of measurement

All primary estimates are in Canadian dollars.

- **Native units.** Statistics Canada records business investment in Canadian dollars.
- **Expenditure.** The World Bank publishes gross national expenditure in both local currency (NE.DAB.TOTL.CN) and current US dollars (NE.DAB.TOTL.CD). For Canada over 1981–2018, the ratio of the two equals the annual average official exchange rate (PA.NUS.FCRF) used in this study to within 0.002. Multiplying the US-dollar series by that rate recovers the local-currency series to within 0.14 percent.
- **FDI.** The World Bank indicator BX.KLT.DINV.CD.WD is published in current US dollars and draws on the IMF Balance of Payments database, supplemented by UNCTAD and official national sources (World Bank n.d.). I express it in Canadian dollars using the annual average official exchange rate.
  - A comparison using data retrieved on 11 November 2026 finds that the resulting series closely tracks Statistics Canada's direct investment liabilities in Table 36-10-0471-01. It is not interchangeable with the directional inward-FDI measure in Tables 36-10-0025-01 and 36-10-0442-01. The distinction concerns the classification of reverse investment and requires explicit documentation (Statistics Canada 2015).
  - The comparison does not identify the IMF's original conversion frequency or independently validate the archived study vintage. Remaining differences may reflect conversion, revisions, source vintages or coverage.
  - Re-estimating the baseline equation with either Statistics Canada series in place of the archived regressor leaves the coefficient sum essentially unchanged (Section 5.8 and the verification note below).
- **Revaluation in US dollars.** Converting to US dollars at a time-varying rate adds a revaluation term to every first difference, as in equation (3). That term captures mechanical exchange-rate revaluation. Write the US-dollar change as ΔI^USD = A + R, where A is the Canadian-dollar spending change converted at the current rate and R is revaluation. Over 1982–2018:
  - Var(A) is 34 percent of Var(ΔI^USD), Var(R) is 31 percent, and 2Cov(A, R) is 35 percent.
  - The correlation between A and R is 0.53, so the revaluation term cannot be read as a separable "share" of variation.
  - In a regression with an intercept, A accounts statistically for about 78 percent of the sample variation in ΔI^USD (R² = 0.778). The remaining 22 percent is the variance share of the component of R orthogonal to A in that regression. It is not the total importance of revaluation, since A and R are correlated.
- **Role of US dollars.** US-dollar estimates are retained as the units of the original study, and are compared with the primary estimates through an exact bridge (Section 5.6).

### 5.2 Benchmark: the original levels specification

The undergraduate study estimated, in US dollars,

  I_t = α + βY_t + γU_t + δFDI_t + ε_t.  (6)

I re-estimate equation (6) by OLS and with AR(1) errors (iterative GLSAR), in both currencies, as a benchmark linking the reconstruction to the original study. The AR(1) model addresses residual persistence under its error specification. It does not make integrated series stationary, establish cointegration, or identify an exogenous inflow shock. The levels coefficient is a static association between trending nominal series. It is not comparable in horizon to the short-run coefficients of Section 5.5.

### 5.3 Stationarity and deterministic terms

ADF tests examine a unit-root null. Lag length is selected by AIC with the software default maximum. A comparison caps the search at three lags and uses BIC. Both settings change in that comparison, so their separate contributions are not identified.

The deterministic terms in each test are chosen to match how the variable enters the estimated equation. Rejecting a unit root around a linear trend does not establish stationarity around a constant, and the primary equation contains no trend.

- For I and Y, levels tests include a constant and trend, and first-difference tests a constant.
- For FDI and U, which enter the primary equation in levels, I report tests with a constant only alongside the trend version, plus a regression of each variable on a linear trend.

In Canadian dollars the results are as follows.

- **I and Y** do not reject a unit root in levels (p = 0.54 and 0.97 with trend), and reject it in first differences (p < 0.001). The primary equation is therefore specified in their first differences.
- **Slack U** rejects a unit root with or without a trend (p = 0.004 with a constant only; p = 0.010 with a trend).
- **FDI** rejects a unit root only around a trend (p < 0.001), not around a constant (p = 0.849). It rises by about C$1.8 billion per year (p < 0.001).

Entering FDI in levels in a trend-free equation therefore imposes the restriction that its trend is offset by other terms. The trend may partly reflect nominal growth of the economy, but that possibility does not remove the need to justify the trend-free equation. I report the linear-trend specification prominently (Section 5.8). ADF outcomes alone do not settle the appropriate deterministic specification in this small sample.

### 5.4 Sample, units and inference

The main dataset contains 38 annual observations for 1981–2018. Differencing and the one-year FDI lag leave 37 observations for the baseline equation, covering 1982–2018. The extension through 2024 provides 43 usable observations. Specifications that add lagged changes in investment and expenditure lose one further year: they use a common 1983–2018 sample of 36 observations, and the baseline is re-estimated on that sample for comparison.

Monetary variables are measured in current-price billions of Canadian dollars. ΔI is an annual change in the nominal investment level, not a percentage growth rate. U is potential minus actual output valued at nominal GDP, in billions; S is the same gap in percent of potential.

Change and error-correction equations use Newey–West HAC standard errors with three lags, Bartlett weights and normal-reference inference. Levels benchmarks use conventional standard errors. HAC estimation addresses error dependence for inference. It does not correct omitted dynamics or endogenous regressors, which the residual diagnostics in Section 5.8 assess directly.

### 5.5 Primary model: change equation with unrestricted FDI timing

**Why a change equation rather than an ECM.** In Canadian dollars, the Engle–Granger test of investment and expenditure does not reject the null of no cointegration under the default lag search (p = 0.382). It does reject under the capped BIC search (p = 0.023). The same pattern holds with N in place of Y (p = 0.394 and 0.024) and in the extended sample. Because the evidence is sensitive to lag-selection settings, I use a change equation as the baseline rather than assume a well-established long-run relation. The primary specification is therefore a change equation without an error-correction term. The ECM is retained as a sensitivity analysis. Its interpretation requires a credible cointegrating relation and an adequate dynamic specification; one significant test alone does not establish validity.

The baseline equation estimates both current and one-year-lagged FDI coefficients. Timing is unrestricted within this two-term specification, rather than over all possible lags:

  ΔI_t = κ + θΔX_t + γU_t + δ₀FDI_t + δ₁FDI_{t−1} + e_t,  (7)

where X is expenditure (Y in the primary specification; N = Y − I in the compositional check of Section 3.3).

Earlier versions of this analysis compared an equation with FDI in levels to one with FDI in first differences, and contrasted their signs. Equation (7) nests both:

  Levels form:   H₀: δ₁ = 0.

  Differences form: H₀: δ₀ + δ₁ = 0  (so that δ₀FDI_t + δ₁FDI_{t−1} = δ₀ΔFDI_t).  (8)

I test each restriction with a Wald test using the HAC covariance. These tests assess whether the restricted forms adequately represent the encompassing equation. Failure to reject a restriction is not evidence that it is true, especially with this sample size. I report:

- **Contemporaneous association:** δ₀.
- **Lagged association:** δ₁.
- **FDI coefficient sum:** δ₀ + δ₁, with a 95 percent interval.  (9)

For a one-year C$1 billion increase in FDI, holding the paths of expenditure changes and slack fixed, the coefficient sum describes the combined association with ΔI in that year and the following year. Equivalently, it describes the resulting investment-level difference after the second year under this equation. A sustained increase in annual FDI has a different implication: after the first year, the coefficient sum applies to each annual investment change. These are model-implied conditional comparisons, not causal responses.

**ECM variant.** Where the error-correction model is estimated, ECT_{t−1} from the regression I_t = a + bX_t + v_t is added to equation (7). When the adjustment process is stable, −(δ₀ + δ₁)/λ describes the eventual displacement of the investment level from its baseline path for a sustained increase in the annual FDI flow, holding the expenditure and slack paths fixed. I report it as a conditional model implication with a delta-method interval, noting the uncertainty in λ and the estimated first-stage residual. The coefficient sum in an ECM is not the full two-year dynamic response, because error correction also operates during that period.

### 5.6 Bridging the Canadian-dollar and US-dollar specifications

Let e_t denote Canadian dollars per US dollar. For monetary series related by Z_t^USD = Z_t^CAD/e_t, multiplication of a US-dollar equation by e_t yields an exact algebraic translation. Separately estimated equations with ordinary constants and unweighted residuals need not be equivalent. In the archived data the conversion identity holds exactly for every monetary series and year. For expenditure it also matches the World Bank's own local-currency series. For FDI, the converted series closely tracks Statistics Canada's native-C$ direct investment liabilities, although the IMF's original conversion method cannot be identified from annual totals (Section 5.1).

For the two-term FDI specification, the exact translated equation is

  e_t ΔI_t^USD = κe_t + θe_t ΔX_t^USD + γU_t^CAD + δ₀FDI_t^CAD + δ₁(e_t/e_{t−1})FDI_{t−1}^CAD + e_t u_t.  (10)

The lagged FDI term uses e_t/e_{t−1} because it was originally converted at the previous year's exchange rate. Weighted least squares with weights e_t^−2, and e_t replacing the ordinary constant, reproduces the US-dollar coefficients when all regressors and observations are translated consistently. In the archived data the translated equation returns a coefficient sum of −0.0251, identical to the directly estimated US-dollar equation.

For any monetary series Z,

  e_t ΔZ_t^USD = ΔZ_t^CAD + (1 − e_t/e_{t−1})Z_{t−1}^CAD.

The second term is the revaluation component in the translated change. The bridge compares the exact translation with equations that apply five adjustments:

- **W:** remove the weights.
- **C:** add an ordinary constant.
- **V:** replace translated changes with Canadian-dollar changes.
- **L:** replace the exchange-rate-adjusted lagged FDI regressor with FDI_{t−1}^CAD.
- **E:** remove e_t.

Applying all five yields the Canadian-dollar baseline exactly (−0.1302). Because the attribution along any one sequence need not be invariant to its order, I estimate all 2⁵ = 32 combinations of adjustments and average each adjustment's contribution over all 120 orders (a Shapley decomposition). I also report the range of its contribution across orders. These ranges describe order sensitivity, not confidence intervals. The attribution is conditional on defining V as one joint adjustment to the investment and expenditure changes. Splitting that adjustment could redistribute its Shapley contribution.

Every design matrix in the decomposition is full rank, including the combinations without either intercept regressor. The largest condition number across all 80 fitted combinations (the three bridges in the Notes table) is 1,371. The outputs of every combination are retained in `drafts/output/bridge_combinations.csv`.

Within this specified set of adjustments, the reported attribution is consistent across orders for the baseline model. Replacing revalued changes with Canadian-dollar changes (V) contributes −0.096 on average, out of a total movement of −0.105, and between −0.084 and −0.108 in every order. The remaining adjustments contribute on average −0.007 (W), +0.020 (C), −0.004 (L) and −0.017 (E). With N in place of Y, V again dominates: −0.076 of a −0.099 total, with range [−0.099, −0.043].

The same translation applied to the levels benchmark, where differencing-induced revaluation terms are absent, moves the FDI coefficient only between 0.109 and 0.124, with no change in sign.

For the variance calculation, write ΔI^USD = A + R, where A is the converted C$ spending change and R is revaluation. Then

  Var(ΔI^USD) = Var(A) + Var(R) + 2Cov(A, R).

Over 1982–2018 the three terms are 34, 31 and 35 percent of Var(ΔI^USD), with corr(A, R) = 0.53. Because the covariance is large, Var(R)/Var(ΔI^USD) is not an additive share of variation explained. The paper therefore reports the decomposition in full and uses the R² of A alone (0.778) as its summary (Section 5.1).

### 5.7 Capacity interaction

To align this exercise with the baseline timing specification, I estimate

  ΔI_t = κ + θΔX_t + γS_t + δ₀FDI_t + δ₁FDI_{t−1} + η₀(FDI_t × S_t) + η₁(FDI_{t−1} × S_t) + e_t.  (11)

S_t is current-year proportional slack, defined as the negative of the HP output gap in percent of potential output. Positive values indicate output below potential. This formulation asks whether current capacity conditions moderate the associations of current and previous-year FDI with current investment changes. All component main effects are included.

At S_t = s, the contemporaneous and lagged marginal associations are

  δ₀ + η₀s, and δ₁ + η₁s, respectively.  (12)

Their sum is a conditional coefficient sum at a common slack value; it is not automatically the response to a one-year inflow change when slack differs across years. I report intervals at the estimation-sample quartiles, a joint test of η₀ = η₁ = 0, and a test of η₀ + η₁ = 0. With only 37 observations, imprecision must be interpreted explicitly.

The contemporaneous-only interaction estimates of earlier drafts are retained as restricted comparisons. The nominal-slack interaction is an additional comparison: multiplying FDI by slack valued at the nominal GDP scale permits the interaction to change with the economy's nominal size even at the same proportional output gap.

**Capacity-slack construction.** The output gap is the cycle from a Hodrick–Prescott filter (λ = 100) applied to log real GDP. Real GDP is in chained 2017 dollars from Statistics Canada Table 36-10-0222-01, and the filter uses the full available series. The archived gap matches the current vintage (1981–2025) to within 0.024 percentage points. Ending the filter at 2018 instead changes the gap by at most 0.57 percentage points (in 2018), with a correlation of 0.998 over 1981–2018. A one-sided gap, computed for each year using only data up to that year, correlates only 0.47 with the full-sample gap over 1990–2018. The slack measure is therefore a retrospective estimate, as discussed in Section 4.3 and Hamilton (2017).

**Interpretation of the interaction results.** The null η₀ = η₁ = 0 is rejected in the timing-aligned model with either expenditure control (joint p < 0.001). This is evidence against constant contemporaneous and lagged slopes within the estimated specification. It should not be described as an absence of moderation simply because some marginal-association intervals include zero. The estimates have opposite signs: η₀ = 0.055 and η₁ = −0.115 with Y, and η₀ = 0.122 and η₁ = −0.188 with N. Thus an additional percentage point of current slack raises the contemporaneous conditional slope and lowers the lagged slope.

Two separate questions must be distinguished. The joint test assesses whether either slope varies with slack. A test of η₀ + η₁ = 0 assesses whether their coefficient sum varies with slack. The HAC Wald test, using Var(η₀) + Var(η₁) + 2Cov(η₀, η₁), gives:
- with Y: η₀ + η₁ = −0.060 (95 percent interval [−0.136, 0.015], p = 0.116);
- with N: η₀ + η₁ = −0.066 ([−0.174, 0.042], p = 0.231).

The data therefore do not reject the hypothesis that the combined FDI association is the same at all slack levels. The two slopes appear to shift in offsetting directions rather than move the combined association.

With Y, the conditional coefficient sum declines from −0.027 at the 25th percentile of slack to −0.201 at the 75th percentile, but all three reported intervals include zero. This concerns the precision of the sum at particular slack values; the test of η₀ + η₁ = 0 above is the direct test of whether the sum differs across slack values. Its interpretation continues to hold slack fixed at a common value, rather than describe an investment response along a changing slack path.

The joint interaction test is sensitive to the treatment of selected years. Adding indicators for 2001 and 2009 raises the joint p-value to 0.110 with Y and 0.035 with N; omitting 2009 gives p = 0.037 with Y. These changes indicate sensitivity to those observations and controls. They do not establish that the pattern is entirely driven by downturns, nor do comparisons of significance alone establish that the underlying coefficients differ across specifications. The interaction coefficients and their intervals for each indicator and omission check are reported in the Notes table alongside the tests. Across those checks, η₁ remains negative and η₀ positive, while the interval for η₀ + η₁ includes zero in every case.

The restricted contemporaneous-only interaction remains insignificant with Y (p = 0.618), whereas the nominal-U timing-aligned interactions are jointly significant (p = 0.002 with Y). The restricted and timing-aligned models test different restrictions, so these findings are not contradictory. Taken together, the estimates suggest an exploratory change in timing with current slack, with no detectable change in the combined FDI association. The specification was developed after observing the baseline results and uses retrospective HP-filtered slack; these features further limit a structural interpretation.

### 5.8 Checks and diagnostics

Each check below targets one threat to the primary FDI estimate and is reported in full.

| Check | Threat addressed |
|---|---|
| Expenditure net of investment (X = N) | Result driven by conditioning on an aggregate containing I (Section 3.3) |
| Linear trend added to equation (7) | Unmodelled FDI trend (Section 5.3) |
| ECM variant (Section 5.5) | Omitted long-run adjustment, if cointegration holds |
| US-dollar estimation and the bridge sequence | Currency-specific valuation dynamics (Section 5.6) |
| Statistics Canada FDI series: direct investment liabilities (1981–2018); directional inward FDI (1991–2018) | Source, vintage and conversion of the World Bank regressor; directional versus asset-liability FDI concept (Section 5.1) |
| Extension to 2024 with a 2020 indicator | Endpoint dependence; the indicator absorbs a 2020 intercept shift only |
| Indicators for 2001, 2009 and 2015 (added after inspecting the data) | FDI peaks in 2000 and 2007 preceding downturns, so that the lagged association reflects the cycle |
| Lagged investment and expenditure changes, on a common 1983–2018 sample | Omitted short-run dynamics |
| Lag-selection settings for ADF and Engle–Granger | Sensitivity of the cointegration conclusion |
| HAC bandwidths 1, 3 and 4 | Sensitivity of inference, with coefficients unchanged |
| Leave-one-out coefficients | Influence of single years; no inference on gapped samples |

Residual serial correlation is assessed with a two-lag Breusch–Godfrey test for every reported equation. HAC errors are not treated as a remedy for it. Failure to reject the test null does not establish independent residuals. Evidence of residual dependence prompts investigation of omitted dynamics. All coefficients remain descriptive regardless of the diagnostic outcome.

No family-wise correction is applied. The checks are diagnostics of one primary model, not independent confirmatory tests.

---

## Notes: results these sections imply (for Sections 6–7, Abstract and Conclusion in step b)

The regression results below were rerun on 11 November 2026 from the archived CSVs with `drafts/revision_checks.py`. The current-source comparisons (Statistics Canada and World Bank) use the `--online` option and data retrieved that day. C$, HAC(3), unless stated. "Coefficient sum" = δ₀ + δ₁. In the change equation, this is a two-year investment-level comparison for a one-year FDI increase; it is not the full two-year dynamic response in an ECM. Main sample n = 37 (1982–2018); extended n = 43.

**Primary model and checks (C$)**

| Specification | δ₀ | δ₁ | p (δ₁=0) | p (δ₀+δ₁=0) | Coefficient sum [95% CI] | BG p |
|---|---|---|---|---|---|---|
| Primary (X = Y) | −0.015 | −0.116 | 0.089 | <0.001 | −0.130 [−0.188, −0.073] | 0.223 |
| X = N | 0.063 | −0.198 | 0.055 | 0.031 | −0.135 [−0.258, −0.012] | 0.274 |
| + linear trend (Y) | 0.014 | −0.064 | 0.329 | 0.324 | −0.050 [−0.150, 0.050] | 0.289 |
| + linear trend (N) | 0.048 | −0.219 | 0.024 | 0.014 | −0.171 [−0.307, −0.034] | 0.295 |
| ECM variant (Y) | 0.006 | −0.104 | 0.089 | <0.001 | −0.098 [−0.153, −0.044] | 0.149 |
| ECM variant (N) | 0.106 | −0.144 | 0.030 | 0.407 | −0.038 [−0.129, 0.052] | 0.018 |
| 2024 + 2020 dummy (Y) | 0.108 | −0.207 | 0.029 | 0.040 | −0.099 [−0.194, −0.004] | 0.367 |
| 2024 + 2020 dummy (N) | 0.194 | −0.276 | 0.026 | 0.238 | −0.081 [−0.216, 0.054] | 0.567 |

**Exploratory downturn-year indicators (baseline, X = Y)**

| Indicators added | δ₁ | Coefficient sum [95% CI] | p | BG p |
|---|---|---|---|---|
| 2009 | −0.084 | −0.095 [−0.173, −0.016] | 0.019 | 0.158 |
| 2001 and 2009 | −0.159 | −0.125 [−0.203, −0.047] | 0.002 | 0.076 |
| 2001, 2009 and 2015 | −0.145 | −0.092 [−0.168, −0.017] | 0.016 | 0.099 |

- Leave-one-out coefficient sums range from −0.155 (dropping 2001) to −0.095 (dropping 2009).
- HAC bandwidths 1, 3 and 4 give intervals of [−0.206, −0.055], [−0.188, −0.073] and [−0.178, −0.082], all p < 0.001.

**Alternative FDI series in the baseline equation (C$; archived I, Y, U unchanged)**

| FDI series | Sample | X = Y: sum [95% CI] | X = Y: BG p | X = N: sum [95% CI] | X = N: BG p |
|---|---|---|---|---|---|
| Archived World Bank × FX (baseline) | 1982–2018, n = 37 | −0.130 [−0.188, −0.073] | 0.223 | −0.135 [−0.258, −0.012] | 0.274 |
| Statistics Canada direct investment liabilities (36-10-0471-01) | 1982–2018, n = 37 | −0.131 [−0.190, −0.072] | 0.222 | −0.135 [−0.260, −0.011] | 0.282 |
| Archived World Bank × FX, same years as directional | 1991–2018, n = 28 | −0.143 [−0.217, −0.069] | 0.377 | −0.201 [−0.330, −0.072] | 0.488 |
| Statistics Canada directional inward FDI (36-10-0442-01, four-quarter sums) | 1991–2018, n = 28 | −0.146 [−0.232, −0.059] | 0.287 | −0.199 [−0.347, −0.050] | 0.460 |

- The directional series begins in 1990, so with the one-year lag its regressions start in 1991. The archived series is re-estimated on the same years for a like-for-like comparison.
- These are current-vintage Statistics Canada series. The archived dataset itself is unchanged.

**Lagged investment and expenditure changes (common sample 1983–2018, n = 36)**

| Specification | Y: sum [95% CI] | Y: BG p | N: sum [95% CI] | N: BG p |
|---|---|---|---|---|
| Baseline on common sample | −0.131 [−0.188, −0.073] | 0.240 | −0.138 [−0.260, −0.017] | 0.335 |
| + lagged ΔX | −0.149 [−0.203, −0.094] | 0.153 | −0.132 [−0.236, −0.028] | 0.329 |
| + lagged ΔI and ΔX | −0.132 [−0.183, −0.080] | 0.001 | −0.153 [−0.249, −0.056] | 0.112 |

- The coefficient sum is stable across these dynamic variants.
- The Y specification containing lagged ΔI and ΔX shows evidence of residual serial correlation (BG p = 0.001); the coefficient-sum stability does not establish adequate dynamics.

**Summary of the evidence**

- The coefficient sum is negative in all 8 timing-unrestricted specifications in the first table and significant at 5 percent in 5 of them. It is also negative and significant in all six common-sample dynamic variants, and with both Statistics Canada FDI series.
- The BG test does not reject no residual serial correlation in the baseline equation (p = 0.223). This is reassuring but does not establish adequate dynamics or justify choosing currency or model form on its own.
- The data reject the differences restriction (p < 0.001). They do not reject the levels restriction at 5 percent (p = 0.089). The lagged point estimate is larger in magnitude, but evidence for its separate contribution is limited.
- The old single-coefficient C$ change equation (FDI_t only) gives −0.107 (p < 0.001). With N it gives −0.085 (p = 0.158), and on the 2024 sample −0.043 (p = 0.481). These estimates impose δ₁ = 0. Compare them with the two-term model using the reported restriction tests; do not dismiss them solely because their significance differs.

**Cointegration (Engle–Granger p, default AIC / BIC cap 3)**

| | 1981–2018 | 1981–2024 |
|---|---|---|
| I ~ Y | 0.382 / 0.023 | 0.291 / 0.004 |
| I ~ N | 0.394 / 0.024 | 0.306 / 0.004 |

**Currency bridge: averages over all 120 orders (Shapley), with range across orders**

| Adjustment | Two-term, X = Y | Two-term, X = N | Contemporaneous only, X = Y |
|---|---|---|---|
| Start: exact US$ translation | −0.025 | −0.036 | 0.001 |
| W: remove weights | −0.007 [−0.015, 0.000] | −0.008 [−0.022, 0.011] | −0.007 [−0.014, 0.000] |
| C: add constant | +0.020 [−0.015, 0.051] | −0.002 [−0.030, 0.041] | +0.024 [−0.011, 0.059] |
| V: C$ changes (drop revaluation) | −0.096 [−0.108, −0.084] | −0.076 [−0.099, −0.043] | −0.102 [−0.115, −0.089] |
| L: unadjusted lagged FDI | −0.004 [−0.007, −0.002] | −0.005 [−0.008, −0.002] | – |
| E: drop e_t | −0.017 [−0.041, 0.016] | −0.006 [−0.043, 0.028] | −0.022 [−0.055, 0.015] |
| End: C$ baseline | −0.130 | −0.135 | −0.107 |

- All 80 fitted combinations are full rank, with a maximum condition number of 1,371 (`drafts/output/bridge_combinations.csv`).
- Levels benchmark: 0.124 (US$) → between 0.109 and 0.119 (C$ steps), no sign change.
- Revaluation decomposition of ΔI^USD, 1982–2018: Var(A) 34%, Var(R) 31%, 2Cov 35%; corr(A, R) = 0.53; R² of A alone = 0.778.
- 2015: C$ change −15.2; US$ change −62.4 = −11.9 (A) + −50.6 (R); rate 1.105 → 1.279.

**Capacity interaction, timing-aligned (equation 11)**

| | η₀ (FDI × S) | η₁ (FDI₋₁ × S) | Joint p | η₀ + η₁ [95% CI], p | BG p |
|---|---|---|---|---|---|
| X = Y | 0.055 (p = 0.065) | −0.115 (p < 0.001) | <0.001 | −0.060 [−0.136, 0.015], 0.116 | 0.342 |
| X = N | 0.122 (p = 0.010) | −0.188 (p < 0.001) | <0.001 | −0.066 [−0.174, 0.042], 0.231 | 0.144 |

Interaction coefficients across indicator and omission checks, with 95% intervals. Omission rows apply HAC to a gapped sequence and are descriptive only.

| X | Check | η₀ [95% CI] | η₁ [95% CI] | Joint p | η₀ + η₁ [95% CI], p |
|---|---|---|---|---|---|
| Y | Baseline | 0.055 [−0.003, 0.113] | −0.115 [−0.177, −0.054] | <0.001 | −0.060 [−0.136, 0.015], 0.116 |
| Y | + 2009 | 0.081 [0.008, 0.153] | −0.155 [−0.276, −0.034] | 0.037 | −0.075 [−0.162, 0.013], 0.094 |
| Y | + 2001, 2009 | 0.070 [−0.002, 0.142] | −0.115 [−0.232, 0.002] | 0.110 | −0.045 [−0.132, 0.042], 0.308 |
| Y | + 2001, 2009, 2015 | 0.099 [0.010, 0.189] | −0.108 [−0.249, 0.034] | 0.065 | −0.008 [−0.085, 0.069], 0.837 |
| Y | Omit 2009 | 0.081 [0.008, 0.153] | −0.155 [−0.277, −0.033] | 0.037 | −0.075 [−0.163, 0.014], 0.098 |
| Y | Omit 2001 | 0.054 [−0.001, 0.108] | −0.089 [−0.138, −0.040] | <0.001 | −0.035 [−0.108, 0.038], 0.344 |
| N | Baseline | 0.122 [0.029, 0.214] | −0.188 [−0.256, −0.119] | <0.001 | −0.066 [−0.174, 0.042], 0.231 |
| N | + 2009 | 0.145 [0.045, 0.246] | −0.224 [−0.411, −0.037] | 0.015 | −0.079 [−0.222, 0.064], 0.278 |
| N | + 2001, 2009 | 0.135 [0.032, 0.237] | −0.186 [−0.379, 0.008] | 0.035 | −0.051 [−0.200, 0.098], 0.503 |
| N | + 2001, 2009, 2015 | 0.177 [0.054, 0.301] | −0.155 [−0.375, 0.064] | <0.001 | 0.022 [−0.098, 0.142], 0.723 |
| N | Omit 2009 | 0.145 [0.045, 0.245] | −0.224 [−0.411, −0.038] | 0.014 | −0.079 [−0.222, 0.064], 0.278 |
| N | Omit 2001 | 0.120 [0.031, 0.210] | −0.162 [−0.225, −0.099] | <0.001 | −0.042 [−0.151, 0.067], 0.452 |

- Adding a 2009 indicator and omitting 2009 give identical point estimates, as expected for a single-year indicator.

Marginal associations at the quartiles of S, with X = Y:

| Quartile of S | S (%) | Contemporaneous [95% CI] | Lagged [95% CI] | Sum [95% CI] |
|---|---|---|---|---|
| p25 | −1.37 | 0.014 [−0.078, 0.105] | −0.041 [−0.146, 0.064] | −0.027 [−0.104, 0.049] |
| p50 | −0.38 | 0.068 [−0.049, 0.186] | −0.156 [−0.239, −0.072] | −0.088 [−0.178, 0.003] |
| p75 | 1.50 | 0.171 [−0.035, 0.377] | −0.372 [−0.512, −0.232] | −0.201 [−0.410, 0.008] |

- Restricted contemporaneous-only interaction: η = −0.015 (p = 0.618) with Y; η = −0.013 (p = 0.827) with N.
- Nominal-U timing-aligned comparison: joint p = 0.002 (Y), p < 0.001 (N).

**US$ comparison (for the bridge section and appendix)**

| | Estimate |
|---|---|
| US$ ECM, FDI_t only | 0.027 (p = 0.615) |
| US$ ECM, coefficient sum | 0.004 [−0.095, 0.103] |
| US$ change equation, coefficient sum | −0.025 [−0.135, 0.085] |

---

## References added or verified in this review

- Government of Canada. *Investment Canada Act*, R.S.C. 1985, c. 28 (1st Supp.), sections 20 and 21. Section 20 supplies the relevant factors; section 21 supplies the likely-net-benefit determination. The wording above avoids suggesting that every foreign acquisition undergoes net-benefit review.
- Rogers, Carolyn. 2024. "Time to break the glass: Fixing Canada's productivity problem." Speech to the Halifax Partnership, Halifax, Nova Scotia, March 26. Bank of Canada. See "The need for investment."
- Statistics Canada. 2008. "Analysis — Fourth quarter 2007." *Canada's Balance of International Payments*, catalogue 67-001-X. Identifies mergers and acquisitions as the main driver of 2007 flows, and energy and metallic minerals as the concentration of fourth-quarter flows. Its historical C$115.4 billion annual total is not a verification of the draft's reconstructed C$129 billion.
- Optional transaction-specific reference: Rio Tinto and Alcan. 2007. "Rio Tinto makes a recommended all cash offer for Alcan." July 12. Company release filed with the US SEC. Supports the announced US$38.1 billion equity offer; it should not be cited as evidence of completion or as a direct measure of that transaction's contribution to Canadian annual FDI flows.

**Additional data and methodological sources**

- Statistics Canada. 2015. "Revisions to Canada's Balance of International Payments." Explains the asset/liability versus directional presentation and the classification of reverse investment.
- Statistics Canada. Table 36-10-0471-01: Balance of international payments, financial account, annual. Selected direct investment liabilities, all countries, Canada; values in millions, divided by 1,000 for billions.
- Statistics Canada. Table 36-10-0442-01: Balance of international payments, direct investment conceptual presentations, quarterly. Selected "Equals: Foreign direct investment in Canada (directional presentation)" and summed four quarters for each calendar year. This table makes the conceptual comparison explicit.
- Statistics Canada. Table 36-10-0025-01: Direct investment flows, quarterly. Selected foreign direct investment in Canada, all countries, total net flows; summed the four quarters. The selected annual values agree with the directional totals from Table 36-10-0442-01.
- World Bank. n.d. BX.KLT.DINV.CD.WD, Canada, and PA.NUS.FCRF, Canada. Retrieved November 11, 2026. FDI metadata.

## FDI conversion verification: current-source comparison

This is a comparison of current public series, independently reproduced by `drafts/revision_checks.py --online`. The World Bank API responses were retrieved on November 11, 2026 and report that date as their last update. Statistics Canada's annual and quarterly table pages report release dates of May 28 and August 27, 2026, respectively. Differences in release vintage remain relevant.

For each year, reconstructed C$ FDI equals BX.KLT.DINV.CD.WD multiplied by PA.NUS.FCRF and divided by one billion. Statistics Canada's annual liabilities come directly from Table 36-10-0471-01. Directional inward flows are calendar-year sums from Table 36-10-0442-01, cross-checked against Table 36-10-0025-01 where available.

| Year | World Bank × annual FX, C$bn | StatCan liabilities, C$bn | StatCan directional inward FDI, C$bn |
|---|---|---|---|
| 2007 | 129.370 | 126.131 | 125.476 |
| 2009 | 23.916 | 23.448 | 25.948 |
| 2015 | 76.710 | 76.272 | 56.057 |
| 2018 | 55.207 | 55.236 | 48.803 |
| 2024 | 86.342 | 86.825 | 91.578 |

Across 1981–2018, the converted current World Bank series and Statistics Canada's annual direct investment liabilities have a correlation of approximately 0.99986. Their mean absolute difference is C$0.242 billion, and their largest absolute difference is C$3.239 billion in 2007. The archived FDI_cad series gives the same statistics, so it matches the current World Bank release over this period. These statistics show a close empirical match, not an exact conversion identity.

In 2015, the gap relative to directional inward FDI is C$20.653 billion, while the gap relative to liabilities is only C$0.438 billion. This strongly suggests that presentation differences matter for selecting the comparator; it does not by itself prove the precise source lineage of every World Bank observation.

**Implication for the paper.** Describe the retained regressor precisely as the World Bank FDI net-inflow indicator expressed in C$. Document its close alignment with direct investment liabilities, and do not label it as an exact reconstruction of Statistics Canada's directional inward-FDI series. Both replacement-series regressions have now been run (Notes table, "Alternative FDI series").
- **Liabilities series.** Replacing the regressor with Statistics Canada's native-C$ liabilities leaves the coefficient sum at −0.131 (−0.135 with N), so the results are not sensitive to the World Bank source or its conversion.
- **Directional series.** Over 1991–2018, the directional inward-FDI series gives −0.146 (−0.199 with N), against −0.143 (−0.201) for the archived series on the same years. The FDI concept therefore does not change the conclusion over the period for which both are available.

**What remains unresolved.** Annual and quarterly conversions cannot be distinguished from these annual totals alone. Remaining discrepancies require matched source vintages, the original conversion documentation and, if available, the underlying higher-frequency flows. The archived study data remain frozen for reproducibility; the replacement-series regressions are reported as a separate check.
