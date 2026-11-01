# Foreign Direct Investment and Business Investment in Canada
## Evidence from Annual Data and Specification Sensitivity

Porokmi Sambahamphe
M.A. Economics student, Fordham University
Extended Working Paper
November 2026

[PAGE]
# Abstract

This extended working paper examines the conditional relationship between foreign direct investment net inflows and business gross fixed capital formation in Canada. The main sample contains 38 annual observations for 1981–2018; an extension covers 1981–2024. Using archived data drawn from Statistics Canada and the World Bank, I estimate levels regressions, an autoregressive error model, error-correction equations, and change equations. The study asks whether FDI is positively associated with investment, whether investment and expenditure share a stable long-run relationship, whether capacity slack moderates the FDI association, and whether the findings survive alternative currencies and specifications. The main US-dollar FDI coefficients are positive but statistically insignificant: 0.124 in OLS, 0.053 with AR(1) errors, and 0.027 in the baseline error-correction model. Canadian-dollar change equations produce negative coefficients near −0.107, but these are sensitive to the sample endpoint and to whether FDI enters in levels or changes. Cointegration evidence is stable for the main US-dollar sample but changes under alternative lag-selection settings elsewhere. Residual serial correlation remains in the baseline error-correction equation and several dynamic variants. An interaction between FDI and capacity slack is not statistically significant. Overall, the evidence does not establish a stable positive FDI–investment association or identify displacement of investment by domestic owners. The contribution is a transparent reconstruction and reassessment of an earlier undergraduate study, with explicit attention to measurement, time-series assumptions, uncertainty, and reproducibility.

Keywords: foreign direct investment; business investment; Canada; cointegration; error correction; specification sensitivity.

# Project scope

This project began as an undergraduate research paper in 2019. I revisited it in 2026 to strengthen my empirical research skills and develop it further for my research portfolio. The extended working paper reconstructs the dataset, moves the analysis from EViews to Python, introduces time-series diagnostics, and reconsiders the interpretation of the original results. This document presents the expanded research draft.

[PAGE]
# Contents

1 Introduction and research questions
2 Literature and the contribution of this study
3 Economic framework and testable hypotheses
4 Data and measurement
5 Empirical strategy
6 Main results
7 Robustness and diagnostic extensions
8 Discussion and policy implications
9 Limitations and future research
10 Conclusion
References
Appendix A Variable construction and sample accounting
Appendix B Reproduction and research transparency
Appendix C Reassessment of the original undergraduate project

[PAGE]
# 1 Introduction and research questions

Foreign direct investment is often discussed as a source of finance, technology, and productive capacity. Yet a recorded inflow and an addition to the capital stock are different economic objects. A new foreign-owned production facility involves new fixed investment. The purchase of an existing firm may generate a large international financial transaction without an equally large addition to fixed assets that year. Foreign participation can also change the investment decisions of suppliers and competitors. Consequently, the relationship between FDI and investment depends on the activities financed and the responses of other firms.

The distinction is especially important when an empirical study relates aggregate FDI inflows to a national-accounts investment series. A positive regression coefficient does not automatically measure new domestic investment caused by foreign capital. A coefficient below one is not, by itself, evidence that domestic investors have been displaced. Interpretation requires compatible measures, appropriate dynamics, and a credible account of the factors that jointly determine foreign inflows and business spending.

I study this relationship for Canada using annual observations for 1981–2018, with an extension through 2024. The dependent variable is business gross fixed capital formation. Gross national expenditure and an estimated capacity-slack variable represent demand conditions and the economy’s position relative to estimated potential output. FDI net inflows are the explanatory variable of interest. The investment series covers business activity located in Canada, including foreign-owned businesses; it does not isolate investment undertaken by Canadian owners.

The project revisits an undergraduate analysis completed in 2019. Rather than present the new work as a direct replication, I distinguish the reconstruction from the earlier dataset and estimator. The original document contains inconsistent sample descriptions, and the revised capacity measure differs from its stated definition. The present analysis therefore asks what the reconstructed evidence supports, not whether an old coefficient can be reproduced to the last decimal place.

## 1.1 Research problem

The central problem is that a simple comparison between FDI and investment can combine financial transactions, business-cycle movements, nominal trends, and exchange-rate changes. If these elements are not separated analytically, a large goodness-of-fit statistic or a significant coefficient may receive an interpretation that the model cannot support. The research task is to evaluate the stability of the conditional association while making those interpretive limits explicit.

The study is deliberately descriptive. It estimates how investment varies with FDI after conditioning on the included regressors. It does not introduce an instrument, policy discontinuity, or other source of plausibly exogenous variation in inflows. This scope permits a useful assessment of model dependence while preventing causal conclusions that would exceed the research design.

## 1.2 Research questions

RQ1. Are annual FDI net inflows associated with business investment in Canada after conditioning on expenditure and estimated capacity slack? I examine the sign, magnitude, uncertainty, and interpretation of the FDI coefficient in the main US-dollar specifications.

RQ2. Is there evidence of a cointegrating relationship between business investment and expenditure, and is that conclusion stable across currency denomination, sample endpoints, and lag-selection settings? This question determines how strongly an error-correction interpretation can be maintained.

RQ3. Does the conditional association between FDI and investment depend on available capacity? I examine an FDI-by-slack interaction and report the implied marginal associations at different observed slack values.

RQ4. How sensitive are the FDI results to currency, dynamic controls, the treatment of FDI as a level or a change, the sample extension, and covariance assumptions? These comparisons assess robustness without treating statistical significance as a model-selection objective.

## 1.3 Objectives and contribution

The first objective is to make the economic estimand precise: business investment within Canada is the outcome, and aggregate financial inflows are the explanatory measure. The second is to reconstruct a transparent dataset and estimation workflow. The third is to assess the assumptions behind levels and error-correction models rather than infer their validity from fit. The fourth is to explain what the empirical instability implies for interpretation.

The contribution is modest but substantive. This is a documented reassessment of an existing question, combining baseline replication with diagnostic extensions. It adds currency-specific stationarity tests, alternative cointegration settings, common-sample dynamic comparisons, covariance sensitivity, and coefficient-influence checks. A finding that a conclusion is not stable is informative when the original interpretation depended on treating a particular coefficient as economically decisive.

The remainder develops the literature and framework, explains the data and methods, presents the main estimates, and examines their sensitivity. The final discussion connects the results to the distinction between attracting financial inflows and increasing productive investment.

[PAGE]
# 2 Literature and the contribution of this study

## 2.1 FDI and aggregate capital formation

Borensztein, De Gregorio, and Lee (1995) examine FDI from industrial economies to 69 developing countries. Their results link FDI to growth through technology transfer, with benefits conditional on a threshold level of human capital. They also report an increase in total investment greater than the FDI inflow. This provides a rationale for complementarity, but its setting and outcome differ from a single-country Canadian time series. The result motivates a possible positive relationship rather than a coefficient that Canada should be expected to reproduce.

Agosin and Mayer (2000) explicitly investigate crowding in and crowding out using developing-country panels for 1970–1996. Their regional findings differ: crowding in is stronger in Asia, while crowding out is prominent in Latin America. Their research highlights heterogeneity rather than a universal investment response. For the present study, the relevant lesson is to test the relationship in its specific setting and to avoid treating a result from one region as a general rule about foreign capital.

The undergraduate project used Van Loo (1977) as its historical Canadian benchmark. That earlier citation frames the continuity of the research question. This extended working paper does not independently reproduce Van Loo’s dataset or estimator, and it does not interpret the difference between historical and reconstructed coefficients as a formal estimate of change over time. Such a comparison would require harmonized definitions and a design that separates period effects from measurement and specification differences.

## 2.2 Evidence specific to Canada

Hejazi and Pauly (2002) study Canadian capital formation with annual industry-level data for 1983–1995 and panel methods. Their aggregate findings associate inward FDI with additional capital formation, while the outward-FDI relationship is not statistically significant for the economy as a whole. They also report heterogeneity across investment components, industries, and trading partners. This is a closer geographical comparison than the developing-country studies, but the industry panel and the aggregate annual models answer different statistical questions.

The contrast matters for research design. An industry panel can distinguish movements across sectors from movements over time, subject to its controls and identifying assumptions. An aggregate time series collapses those differences into one annual observation. Positive expansion in one sector can coexist with reduced spending elsewhere. Therefore, a national coefficient cannot reveal whether foreign entry is complementary in supplier industries but competitive in the same product market. Disaggregation is a substantive extension, not merely a way to increase sample size.

## 2.3 Firm linkages and the limits of aggregation

Javorcik (2004) uses Lithuanian firm-level data to examine productivity spillovers through backward linkages. The results are consistent with gains for domestic suppliers connected to foreign affiliates, particularly where ownership is shared. The outcome is productivity, not the aggregate investment measure used here. The study nonetheless provides a concrete reason to distinguish supplier channels from effects on competitors: foreign participation can affect different domestic businesses through different relationships.

Desai, Foley, and Hines (2005) examine outward FDI and domestic capital spending. Cross-country evidence and firm-related US time-series evidence point in different directions. Their analysis illustrates how the level of aggregation and omitted factors can affect apparent substitution or complementarity. Because the direction of investment is outward, it should not be counted as direct evidence on inward FDI in Canada. Its relevance here is methodological: changing the unit of observation can change what a coefficient represents.

## 2.4 Implications for this extended working paper

The literature suggests several possible mechanisms but does not identify the correct sign for the present sample in advance. Financing and supplier relationships can support investment; competition and financial substitution can work in the opposite direction. The studies also use different outcomes, countries, time periods, and identification strategies. A credible comparison must preserve these differences instead of listing positive and negative estimates as though they measured the same parameter.

This extended working paper is not a comprehensive systematic review or a frontier contribution to the entire FDI literature. It uses a focused set of established studies to motivate its mechanisms and interpret its limited evidence. Its empirical contribution is the close examination of one reconstructed Canadian application. The main research gap addressed is therefore the reliability of the project’s own inference: whether a conclusion about complementarity survives a more careful treatment of measurement and time-series assumptions.

[PAGE]
# 3 Economic framework and testable hypotheses

## 3.1 Investment demand and available capacity

A simple accelerator interpretation connects investment to expected demand. When firms expect sales to expand, they may seek a larger productive capital stock. Actual spending need not adjust immediately because planning, financing, installation, and uncertainty can delay projects. Gross national expenditure is included as a broad demand correlate. It is an imperfect proxy for expected sales, and its contemporaneous relationship with investment cannot be interpreted as an exogenous demand response.

Capacity conditions may also matter. A firm with substantial unused capacity can meet additional orders without immediately purchasing more equipment. At the aggregate level, greater estimated slack can therefore be associated with lower investment, conditional on expenditure. Conversely, an economy near full capacity may face stronger incentives to expand capacity. These considerations motivate a negative coefficient on the slack measure in the baseline model, while recognizing that the aggregate variable is only an estimated output-gap proxy.

Foreign investment can operate through several channels. New projects may directly increase foreign-owned fixed investment. Acquisitions can reorganize existing assets and potentially lead to later spending. Supplier demand may encourage other firms to expand, while stronger competition can reduce some incumbents’ expected returns. Financial inflows may relax funding constraints, or they may substitute for domestic borrowing. The net aggregate association is therefore not signed unambiguously by theory.

## 3.2 Why the coefficient need not be compared with one

An illustrative accounting decomposition helps clarify the issue. Let total business investment equal spending by domestically owned firms plus spending by foreign-owned firms. Suppose, additionally, that a measured FDI inflow equals new foreign-owned fixed investment dollar for dollar. Only under that strong additional assumption would the total-investment response to FDI equal one plus the response of investment by domestic owners.

[EQ] I = Iᴰ + Iᶠ; if FDI = Iᶠ, then ∂I/∂FDI = 1 + ∂Iᴰ/∂FDI. (1)

Equation (1) is an illustrative decomposition, not an identity satisfied by the dataset. FDI net inflows include financing transactions and do not equal foreign-owned fixed capital formation. The dependent variable also does not separately observe either ownership component. A coefficient below one can therefore arise without displacement of domestic owners, and a positive coefficient cannot reveal which ownership group changed its spending.

A causal version of the derivative would require still more assumptions about counterfactual investment in the absence of the inflow. For example, a foreign acquisition might be followed by investment that would otherwise have occurred under domestic ownership. Observing both a financial inflow and spending does not establish additionality. This is why the extended working paper interprets regression coefficients as conditional associations and avoids translating them into domestic crowding-out estimates.

## 3.3 Conditional effects and the role of demand controls

Including expenditure changes the question. If FDI affects investment partly by expanding demand, conditioning on expenditure can remove part of that pathway. Meanwhile, if expected growth attracts foreign investors and raises expenditure, controlling for demand may reduce one source of confounding. These possibilities cannot be distinguished automatically from a regression coefficient. The control is economically motivated, but its inclusion does not establish that the remaining FDI variation is exogenous.

The fact that expenditure includes investment adds a separate accounting complication. The coefficient on expenditure combines behavioral comovement with a shared component. Strong fit may partly reflect that structure. Accordingly, the model is not a structural investment equation with independently identified demand, financing, and competition channels. It is a parsimonious conditional description of aggregate data.

## 3.4 Hypotheses and interpretation rules

For RQ1, the null hypothesis is that the conditional FDI coefficient is zero. A positive, precisely estimated coefficient would support a positive association within the specified equation; it would not, by itself, establish a causal investment multiplier. Failure to reject the null is compatible with zero or with economically relevant values that the sample estimates imprecisely.

For RQ2, the test null is no cointegration between investment and expenditure. Rejection supports an error-correction interpretation under the maintained integration and deterministic specifications. Sensitivity to lag-selection settings weakens a claim that the long-run relationship is an invariant feature of the data.

For RQ3, the null is a zero FDI-by-slack interaction coefficient. A positive estimate would be consistent with a stronger FDI association where spare capacity is greater. That hypothesis is distinct from the negative baseline association between slack and investment. The marginal FDI association must include both the FDI coefficient and its interaction with the observed slack value.

For RQ4, I report stability rather than define success as repeated rejection of a null. Changing FDI from a level to a change changes the estimand. Extending the sample changes both information and economic conditions. A robustness discussion should distinguish those changes from pure adjustments to the standard-error estimator.

[PAGE]
# 4 Data and measurement

## 4.1 Sources and sample construction

The main dataset contains 38 annual observations from 1981 to 2018. An extended dataset contains 44 observations through 2024. Business gross fixed capital formation, nominal GDP, and real GDP originate in Statistics Canada Table 36-10-0222-01. The World Bank provides gross national expenditure, FDI net inflows, and the annual average exchange rate. The replication package includes the archived processed datasets, which preserve the values used in estimation.

The Statistics Canada source is annual and reports national-accounts amounts in millions. The processing code converts investment and nominal capacity slack to billions. World Bank expenditure and FDI are provided in current US dollars and divided by one billion. The exchange rate is Canadian dollars per US dollar. These transformations are recorded explicitly because a coefficient is interpretable only relative to the scale of both its dependent and explanatory variables.

[TABLE variables]

The FDI measure follows the World Bank’s balance-of-payments definition: equity capital, reinvested earnings, and other capital associated with a direct-investment relationship. The metadata uses a voting-interest threshold of at least 10 percent as the criterion for that relationship. This is a financial concept rather than a direct tally of newly constructed physical assets (World Bank, n.d.). The outcome, by contrast, measures gross fixed capital formation. Gross investment should not be confused with net additions after depreciation.

The main dataset has no missing values in its estimation columns. The overlap between the main and extended datasets is numerically identical within floating-point tolerance. I also verify that each CAD monetary series equals its USD counterpart multiplied by the recorded exchange rate. These checks establish internal consistency of the archived files; they do not independently validate the historical source vintage.

## 4.2 Currency denomination

Let e denote CAD per USD. Canadian-dollar investment and slack are divided by e to obtain US-dollar values. US-dollar expenditure and FDI are multiplied by e to obtain Canadian-dollar values. A fixed exchange rate would simply change the units. A rate that varies over time also changes movements in the series and their first differences.

[EQ] Iᵁˢᴰₜ = Iᶜᴬᴰₜ / eₜ. (2)
[EQ] ΔIᵁˢᴰₜ = ΔIᶜᴬᴰₜ / eₜ + Iᶜᴬᴰₜ₋₁(1/eₜ − 1/eₜ₋₁). (3)

Equation (3) is an algebraic decomposition of the currency conversion. It shows that a change in USD investment includes both the CAD change valued at the current exchange rate and the revaluation of the previous level. Adding an exchange-rate level to a regression does not reproduce this identity. The currency models are therefore alternative specifications, not interchangeable estimates expressed in different labels.

## 4.3 Estimated capacity slack

The archived construction applies an HP filter to the full available series of log real GDP, using a smoothing parameter of 100. If τ is the filtered trend, the cycle is log real GDP minus τ. Exponentiating the cycle yields actual output relative to estimated potential. The resulting gap is valued at the nominal GDP price scale to obtain slack in monetary units.

[EQ] cₜ = ln(GDPₜ,real) − τₜ; gₜ = exp(cₜ) − 1. (4)
[EQ] Uₜ = GDPₜ,nominal[1/(1 + gₜ) − 1]. (5)

Positive U means actual output is below estimated potential. Positive gap_pct in the archived data means the reverse: output is above potential. The signs are intentionally opposite. This is an aggregate output-gap-based proxy, not a direct survey measure of unused plant capacity. The monetary scaling can itself introduce persistence even if the underlying proportional cycle is stationary.

Hamilton (2017) explains that HP filtering can generate misleading dynamics and substantial endpoint effects. Here the full-series filter also uses information unavailable at earlier dates. The extended working paper therefore treats U as an estimated retrospective control rather than a real-time policy signal. The complete historical real-GDP input is not archived in the processed files, so a faithful one-sided reconstruction cannot be claimed from these CSVs alone.

## 4.4 Descriptive evidence

[TABLE descriptive]

In the main US-dollar sample, business investment averages about $174.9 billion, compared with $26.4 billion for annual FDI inflows. FDI has a standard deviation slightly larger than its mean and reaches approximately $120.5 billion in 2007. The large variation cautions against describing a single year as representative. Investment and expenditure also rise substantially in nominal terms over the sample, motivating formal consideration of their time-series properties.

[FIGURE series]

Figure 1 illustrates the different behavior of the two series. Investment moves with a broad trend and sizable cyclical changes, while FDI contains pronounced episodes. The plot does not identify the transactions behind those episodes. In particular, it should not be used to classify a peak as greenfield investment or acquisition activity without transaction-level evidence. The lower panel displays the estimated output gap used in constructing U.

## 4.5 Data provenance and comparability

The archived files are sufficient to reproduce the estimation stage. They do not include a recorded original retrieval date or all raw source inputs. Downloading current values can alter the result through data revisions and the full-series capacity filter. The replication package therefore separates reproducing the archived analysis from rebuilding the source data. It records file hashes and software versions for the calculations reported here.

The original undergraduate paper is preserved separately. Several of its EViews estimation tables list 1981–2016 with 36 observations, although parts of the narrative refer to 1981–2018. The present sample’s 38 observations are explicitly dated. This inconsistency, the changed capacity measure, and the different AR(1) estimator prevent a clean interpretation of old-versus-new coefficient differences as economic change.

[PAGE]
# 5 Empirical strategy

## 5.1 Baseline levels regressions

The starting specification relates business investment to expenditure, slack, and FDI. I estimate it first by OLS and then with AR(1) errors using iterative GLSAR. The autoregressive model addresses residual persistence under its error specification. It does not make integrated series stationary, establish cointegration, or identify an exogenous inflow shock.

[EQ] Iₜ = α + βYₜ + γUₜ + δFDIₜ + εₜ. (6)

The expected signs of β and γ are positive and negative respectively. The sign of δ is left to the evidence. The models are useful as benchmarks because they make the relation to the undergraduate specification visible. They are not treated as definitive simply because they fit the levels closely. Conventional uncertainty estimates are retained for these historical baseline comparisons, while the change and error-correction equations use HAC covariance estimates.

## 5.2 Stationarity and lag selection

ADF tests examine a unit-root null. Levels tests include a constant and trend; first-difference tests include a constant. The baseline selects lags by AIC using the software’s default maximum. A diagnostic comparison caps the maximum at three and selects by BIC. Both the cap and criterion change in that comparison, so their separate contributions cannot be identified from it. The reported lag lengths and effective observations make the cost of the selected dynamics visible (statsmodels, n.d., adfuller documentation).

The short annual sample is central to interpretation. A test that uses seven or eight lagged differences consumes considerable information. Non-rejection does not prove a unit root, and rejection under a particular deterministic specification does not prove stationarity under every plausible alternative. I therefore use the tests to organize model choices and expose sensitivity, rather than as an automatic classification algorithm.

## 5.3 Cointegration and error correction

Following the two-step framework of Engle and Granger (1987), I estimate a long-run investment–expenditure regression and construct its lagged residual. Cointegration means that a stationary combination can exist even when the individual series are integrated. The relevant null is no cointegration, and the residual-based test requires its own critical values rather than an ordinary residual ADF interpretation. The software implementation applies the augmented Engle–Granger procedure (statsmodels, n.d., coint documentation).

[EQ] Iₜ = a + bYₜ + vₜ; ECTₜ₋₁ = Iₜ₋₁ − â − b̂Yₜ₋₁. (7)
[EQ] ΔIₜ = κ + θΔYₜ + γUₜ + δFDIₜ + λECTₜ₋₁ + eₜ. (8)

The error-correction term is the previous year’s deviation from the estimated investment–expenditure relation. A negative λ is consistent with adjustment toward that relation. FDI and U enter equation (8) in levels and are not included in the estimated cointegrating vector. The FDI coefficient therefore describes an association with the annual investment change, conditional on demand changes, slack, and the lagged deviation; it is not a long-run FDI multiplier.

The familiar adjustment interpretation requires qualifications. It is conditional on the other regressors and on an adequate dynamic specification. A negative coefficient cannot rescue residual misspecification or make a lag-sensitive long-run relation definitive. The two-step generated regressor also introduces estimation uncertainty not fully characterized by quoting a single conventional second-stage p-value in a small sample.

## 5.4 Capacity interaction

[EQ] ΔIₜ = κ + θΔYₜ + γUₜ + δFDIₜ + η(FDIₜ × Uₜ) + λECTₜ₋₁ + eₜ. (9)
[EQ] Conditional marginal FDI association at U = u: δ + ηu. (10)

The interaction model retains both main effects. Its FDI coefficient is the marginal association at zero slack, not the average effect across all years. I report the interaction test and marginal associations at the first quartile, median, and third quartile of slack in the estimation sample. Confidence intervals use the covariance between δ and η. This avoids interpreting a positive interaction estimate as evidence of a statistically established pattern when the uncertainty remains wide.

## 5.5 Robustness design and diagnostics

The sensitivity analysis follows several distinct comparisons. First, I re-estimate the models in CAD and extend the endpoint to 2024. Extended-sample regressions include a 2020 indicator, which absorbs an intercept shift for that year rather than an entire pandemic transmission mechanism. Second, I compare fixed dynamic variants on common observations: the baseline ECM, an added lagged expenditure change, and added lagged changes in both investment and expenditure. All common-sample comparisons start in 1983.

Third, change equations omit ECT and compare FDI in levels with FDI in first differences. These answer different questions. Fourth, HAC bandwidths of one, three, and four are compared without altering the fitted coefficients. The default HAC estimates use three lags, Bartlett weights, normal-reference inference, and no small-sample covariance correction in the regression fit. HAC covariance estimation addresses certain error dependence for inference; it does not correct omitted regressors or endogenous right-hand-side variables.

Finally, the two-lag Breusch–Godfrey test assesses residual serial correlation. Leave-one-out calculations examine coefficient influence while holding the constructed variables fixed. Since deletion leaves gaps in calendar time, I report only the influence coefficients, not HAC significance tests on the compressed sequence. Every comparison is retained in the replication outputs. A model is not selected because its FDI p-value is smallest or because one diagnostic happens to cross a conventional threshold.

[PAGE]
# 6 Main results

## 6.1 Time-series evidence

[TABLE adf]

In both currencies, the main-sample levels tests fail to reject unit roots for investment and expenditure at 5 percent under both lag-selection settings. For the US-dollar default tests, the p-values are 0.136 and 0.061. The second value is close to a conventional threshold and should not be summarized as unambiguous evidence of a unit root. Under the capped BIC comparison, the corresponding p-values are 0.451 and 0.555.

FDI and slack reject the levels unit-root null under the tested main-sample settings in both currencies. The CAD slack p-value changes from 0.010 to 0.029, while FDI remains below 0.001. For investment and expenditure, first-difference tests reject unit roots under both settings, with main-sample p-values below 0.001. These findings are consistent with the baseline treatment of I and Y as I(1) and FDI and U as stationary controls, subject to the limitations of the tests.

The exchange-rate level does not reject a unit root at 5 percent in the tested main-sample specifications. Its p-value is 0.075 under default AIC and 0.335 under the capped BIC comparison. A CAD change equation that includes the exchange-rate level therefore requires separate caution; adding that control is not automatically a stationarity-preserving robustness correction.

[TABLE cointegration]

The main US-dollar investment–expenditure test gives p = 0.002 under both settings. The other samples are much more sensitive. The CAD main-sample p-value moves from 0.382 under default AIC to 0.023 under the capped BIC setting. For the extended USD sample it moves from 0.358 to below 0.001; for extended CAD, from 0.291 to 0.004. These reversals are a substantive finding of the extended working paper’s diagnostic extension.

It would be misleading either to declare that CAD cointegration is absent or to select the alternative settings solely because they produce rejection. The defensible conclusion is that the evidence outside the main USD sample depends strongly on the tested lag-selection configuration. All ECM results are therefore interpreted alongside these diagnostics, with additional caution for the currency and endpoint comparisons.

## 6.2 Baseline FDI estimates

[TABLE baseline]

The baseline FDI coefficient is 0.124 in OLS and falls to 0.053 after the AR(1) error specification. Their p-values are 0.156 and 0.405. In the 37-observation USD ECM the coefficient is 0.027, with a HAC standard error of about 0.054 and p = 0.615. None rejects a zero FDI coefficient at 5 percent. The decline across estimators illustrates why the initial levels relationship should not be interpreted without its dynamics.

The ECM estimate has a straightforward scale interpretation. Annual FDI inflows that are US$1 billion higher are associated with approximately US$0.027 billion more annual change in business investment, holding the included regressors fixed. The interpretation concerns the inflow level, not a US$1 billion increase in FDI from the preceding year. The estimate is not an elasticity and does not imply that foreign capital created that spending.

Statistical insignificance also needs a scale interpretation. The approximate 95 percent interval for the baseline ECM spans negative and positive values. It does not rule out all economically meaningful associations. The result is evidence of limited precision around a small point estimate, not proof that the true contribution of FDI is exactly zero. A policy argument that FDI has no economic value would go well beyond these estimates.

[FIGURE coefficients]

## 6.3 Expenditure slack and adjustment

The ECM expenditure-change coefficient is approximately 0.224 and is positive. This is consistent with investment moving with demand conditions, but the accounting overlap and simultaneous determination prevent a structural interpretation. The slack coefficient is −0.174, with HAC p = 0.078. Its sign agrees with the baseline expectation, while its uncertainty prevents a strong 5 percent rejection of zero.

The error-correction coefficient is −0.369 (p = 0.019). Under the fitted equation, about 37 percent of a prior deviation from the estimated investment–expenditure relationship is corrected over one year, conditional on the short-run controls. This percentage describes the adjustment term rather than the FDI association. It should not be interpreted as 37 percent of an FDI shock being absorbed annually.

The residual diagnostic qualifies this attractive adjustment interpretation. The baseline ECM’s Breusch–Godfrey p-value is approximately 0.001. Remaining serial correlation indicates that the conditional mean or error structure has not been fully captured. HAC inference does not remove that concern. The result supports further dynamic investigation rather than a declaration that the long-run mechanism has been fully established.

[PAGE]
# 7 Robustness and diagnostic extensions

## 7.1 Currency and the FDI transformation

[TABLE currency]

The CAD change equation without ECT gives an FDI coefficient of −0.107 (p = 0.0006). Adding the exchange-rate level leaves the estimate at −0.108 (p = 0.0004). In the latter equation, inflows that are C$1 billion higher are associated with a C$0.108 billion smaller annual change in business investment, conditional on the controls. This is a negative conditional association in those equations, not identified displacement of investment by Canadian owners.

The difference from USD is not resolved by the extra exchange-rate term. Equation (3) shows why the USD change contains a revaluation component. Moreover, the estimated cointegrating residual changes across currencies, so the ECM comparison involves more than the FDI column alone. Correlated valuation movements, nominal scaling, and model restrictions can all affect the regression. The estimates do not isolate the contribution of any one explanation.

Changing FDI to its annual difference reverses the main-sample CAD point estimate to about 0.080, with p = 0.258. The comparable USD change coefficient is about 0.113, with p = 0.062. These are not robustness estimates of precisely the same parameter: they relate investment changes to changes in inflows. Their value is to show that the negative levels-FDI result is not a general statement about every reasonable meaning of an FDI increase.

## 7.2 Sample extension and pandemic control

Extending through 2024 changes the CAD levels-FDI association substantially. With the 2020 indicator, the CAD change-equation coefficient becomes approximately −0.043 (p = 0.481). The USD levels-FDI ECM coefficient remains small and insignificant at 0.032 (p = 0.548). These results do not support treating the original CAD negative association as a stable relationship over the entire extended period.

There is also evidence that complicates a blanket claim of no FDI association. In the extended USD change equation with differenced FDI, the coefficient is about 0.146 and p = 0.031. Its two-lag residual test does not reject no serial correlation. Extended CAD gives a positive differenced-FDI coefficient of about 0.173 with p = 0.062. These findings must be reported even though they do not match the baseline narrative. They concern a different regressor transformation and remain descriptive.

A single indicator for 2020 is limited. It permits an intercept shift in that year but cannot capture changing behavioral slopes, multiple pandemic years, recovery dynamics, or all other changes between 2019 and 2024. The additional observations are informative, yet the extended model is not a controlled experiment that identifies why the coefficient changes. This is one reason to present the extension as a sensitivity exercise rather than evidence of a dated structural break.

## 7.3 Dynamic controls and residual dependence

[TABLE dynamics]

Common-sample USD estimates reduce the FDI coefficient from 0.036 in the baseline to 0.027 with lagged expenditure changes and 0.010 with lagged investment and expenditure changes. All remain statistically insignificant. However, their Breusch–Godfrey p-values are about 0.0007, 0.0003, and 0.024. Adding those lags does not eliminate residual dependence at 5 percent in the main sample.

The same caution applies to the CAD dynamic variants. Their negative coefficients do not become compelling causal evidence merely because additional terms were included. A lagged dependent variable alongside serially correlated errors can create further estimation problems, so a richer-looking equation is not necessarily better specified. The comparison shows the limits of these particular variants rather than proving that no adequate dynamic model is possible.

[FIGURE residual_acf]

Residual autocorrelation plots supplement the formal tests by showing dependence over several lags. With a short sample, neither the plots nor individual p-values should be interpreted mechanically. A useful next stage would compare a deliberately small set of justified lag structures, evaluate parameter stability, and consider alternative measures of demand and real activity. That stage should be motivated by the economic process, not by searching until the desired FDI sign appears.

## 7.4 Capacity interaction and marginal associations

[TABLE interaction]

The FDI-by-slack coefficient is approximately 0.003, with p = 0.267 in the baseline interaction model. The implied FDI associations increase across the observed slack distribution: about 0.032 at the first quartile, 0.062 at the median, and 0.105 at the third quartile. Nevertheless, all three 95 percent intervals include zero. The extended working paper therefore does not establish that capacity slack moderates the FDI association.

This conclusion is narrower than saying the mechanism is absent. The interaction is estimated with few observations, a noisy capacity proxy, and unresolved residual dependence. The expected pattern in the point estimates can be described, but it should not be promoted to a result supported by precise statistical evidence. In particular, the largest marginal estimate also has the widest interval, so its numerical size does not make it the most reliable finding.

## 7.5 Covariance and coefficient influence

[TABLE hac]

Changing the HAC bandwidth leaves the coefficients unchanged but alters their standard errors. The USD baseline remains insignificant for bandwidths one, three, and four, with p-values near 0.575–0.615. The CAD negative change coefficient remains significant at 5 percent in these checks, but its p-value ranges from about 0.014 to below 0.001. This demonstrates why an exact p-value should not be treated as a measure of economic stability.

The leave-one-out USD baseline coefficients range from approximately −0.001 to 0.045. The CAD change-equation coefficients remain negative, ranging from about −0.131 to −0.071. Thus the CAD sign is not attributable to deleting just one observation under this particular conditional calculation. That does not resolve its sensitivity to the endpoint or regressor transformation. Constructed gap and error-correction variables are held fixed, and no inferential p-values are assigned to the gapped deletion samples.

## 7.6 Answers to the research questions

For RQ1, the main USD models do not provide precise evidence of a positive conditional FDI coefficient. For RQ2, main USD cointegration evidence is stable across the two tested configurations, whereas other currency and endpoint results are lag-setting sensitive. For RQ3, the interaction does not provide statistically established moderation by slack. For RQ4, the currency, endpoint, and transformation comparisons demonstrate material instability, while some coefficient signs survive narrower covariance and single-observation checks.

These answers deliberately distinguish between types of robustness. A result can survive one observation being removed yet fail to survive extending the period. It can remain significant under different standard errors while referring to a parameter that changes meaning under differencing. The research conclusion rests on that full pattern rather than a count of significant coefficients.

[PAGE]
# 8 Discussion and policy implications

## 8.1 What the evidence supports

The strongest conclusion is about interpretation. The aggregate data do not deliver one stable FDI–investment coefficient across the examined equations. The original positive levels association weakens after accounting for persistence and adjustment. A negative CAD association is present in some models, but it attenuates in the extended sample and changes sign when the regressor becomes the change in FDI. Positive evidence appears in one extended USD change model, preventing a universal claim that no association exists anywhere in the analysis.

This pattern does not imply that every model is equally credible. The cointegration results and residual diagnostics provide reasons to treat some interpretations more cautiously than others. Yet they also do not identify a single model that fully resolves the research problem. The extended working paper’s contribution is to make those differences visible and to restrict the substantive claim accordingly.

The distinction between financing and capital formation provides an economic explanation for why an aggregate coefficient may be unstable, but it is not tested directly here. Variation in acquisition shares, sectoral composition, financing choices, or investment timing could matter. Without the corresponding data, these remain plausible mechanisms rather than established explanations for the estimated sign reversals.

## 8.2 Implications for evaluating FDI policy

The results do not justify estimating the return to an FDI subsidy or the investment loss from restricting a transaction. No policy intervention is identified, and the financial inflow series does not measure the projects receiving such treatment. Applying a regression coefficient to a proposed subsidy would add assumptions about selection, additionality, and behavioral responses that the study has not tested.

The descriptive evidence instead supports a measurement priority. Evaluating productive investment requires distinguishing new capacity from ownership transfers, observing follow-on spending, and tracking the responses of suppliers and competitors. An acquisition can be followed by modernization and beneficial reorganization, so a transaction that does not immediately create fixed capital should not automatically be classified as economically unproductive. Equally, a large recorded inflow is not sufficient evidence of additional domestic capacity.

The literature provides mechanisms involving technology and supplier relationships, but this study cannot measure their welfare contribution. Productivity gains, employment, wages, tax revenue, and competitive effects are separate outcomes. A weak investment coefficient does not prove an absence of those benefits; a positive investment coefficient does not demonstrate that benefits exceed policy costs. The policy relevance is to improve the questions and data used for appraisal, not to announce a universal rule for welcoming or rejecting foreign ownership.

## 8.3 Implications for empirical research

A useful lesson from the reconstruction is that stronger research does not always mean a stronger headline result. More careful methods can weaken an original claim, uncover sensitivity, and reveal why a simple economic interpretation was premature. In this application, documenting the data definitions and confronting residual diagnostics are at least as important as adding an advanced estimator.

The next research design should begin with the outcome and the counterfactual. If the objective is displacement of domestic owners, ownership-specific capital expenditure is needed. If it is the contribution of greenfield inflows, entry-mode information and project timing are needed. If it is a causal policy effect, the design must explain which variation is plausibly independent of firms’ expected investment opportunities. Those decisions should precede the selection of an econometric technique.

[PAGE]
# 9 Limitations and future research

## 9.1 Identification and measurement

Endogeneity is the main limitation. Expectations of demand can attract foreign capital and stimulate investment at the same time. Investment plans can also precede and help attract inflows. Controlling for observed expenditure does not guarantee that all relevant expectations, costs, and financing conditions have been accounted for. Without a credible source of exogenous variation, reverse causality and omitted variables remain viable explanations for the estimates.

The investment and FDI variables are not ownership-matched components of a common accounting identity. Investment includes spending by foreign-owned firms, while net inflows include financial transactions that need not represent new fixed assets. This mismatch is not a minor measurement error that can be repaired by changing units. It limits the very question that can be answered about crowding out. Future ownership and entry-mode data would improve the estimand before additional controls improve its estimation.

Nominal scaling is another unresolved issue. Both domestic inflation and exchange-rate movements can affect current-dollar series. Cointegration among nominal aggregates does not automatically describe a stable relation among real quantities. A future analysis should obtain compatible real investment and demand measures, document their deflators, and reassess the integration assumptions. Dividing all variables by a convenient common denominator would introduce its own restrictions and should not be presented as an automatic solution.

## 9.2 Dynamics and finite-sample uncertainty

The main sample is small for the number of decisions involved: deterministic trends, lag selection, cointegration testing, interaction terms, and robust covariance estimates. Asymptotic tests can be imprecise in that setting. Multiple specification comparisons also increase the opportunity to find an isolated significant result. Reporting the complete planned set of comparisons reduces selective presentation, but it does not turn the collection of p-values into a joint confirmatory experiment.

Serial correlation remains in the main ECM and several lag variants. This limits confidence in adjustment-speed and short-run coefficient interpretations. More lags are not a free correction because they consume degrees of freedom and may introduce additional bias when errors remain dependent. A defensible extension should justify a parsimonious dynamic structure, inspect stability, and report failures rather than suppress them.

The HP-derived capacity measure is estimated rather than observed. Filtering choices and the full-series information set affect it, while the processed archive does not permit a full real-time reconstruction. Alternative potential-output measures or independently observed utilization data would provide a more substantive sensitivity exercise than repeatedly changing the filter parameter without economic justification.

## 9.3 A feasible next research stage

A first extension would preserve the archived nominal analysis as a benchmark and construct a documented real-CAD dataset with compatible sources. It would also retain the raw files, retrieval dates, metadata, and transformations needed to rebuild every derived measure. This would separate valuation effects from changes in physical investment more clearly while preserving reproducibility.

A second extension would investigate disaggregation. Industry-level capital spending combined with inward-FDI measures could examine whether the aggregate coefficient masks differences across sectors. The unit of observation, weighting, and treatment of common macroeconomic shocks would need to be stated explicitly. More observations alone would not establish causal identification, and findings for one industry should not be generalized automatically to the economy.

A third extension would design an identification strategy around a specific mechanism or institutional change. Such a design might require policy eligibility rules, transaction-level information, or firm panels with credible comparison groups. An instrument should be defended through its exclusion restriction, not proposed merely because it predicts FDI. The present extended working paper lays out these requirements but does not claim to have executed them.

[PAGE]
# 10 Conclusion

This extended working paper reconstructs and reassesses the relationship between FDI net inflows and business investment in Canada. The main evidence comes from 38 annual observations for 1981–2018, with an extension through 2024. The research distinguishes the conditional FDI association, the investment–expenditure long-run relationship, capacity moderation, and specification sensitivity rather than treating one coefficient as a complete answer about foreign investment.

The main USD estimates are positive but statistically insignificant, ranging from 0.124 in OLS to 0.027 in the baseline ECM. The negative CAD levels-FDI association is present in the main-sample change equations, but it weakens with the extended endpoint and differs from results using changes in inflows. Cointegration outside the main USD sample is sensitive to the tested lag-selection settings. The capacity interaction is imprecisely estimated, and serial correlation remains an unresolved feature of important specifications.

Consequently, the study does not establish a stable positive aggregate association or identify displacement of domestic owners’ investment. It also does not demonstrate that FDI is economically irrelevant. The estimates are conditional, model-dependent descriptions of financial inflows and business spending, and some alternative change specifications provide positive evidence that must be acknowledged.

The methodological contribution is a transparent account of what changed when the undergraduate analysis was reconstructed and its assumptions were tested. The substantive implication is that attracting financial inflows and expanding productive capacity are related but distinct policy objectives. Stronger conclusions require better-matched investment data, explicit treatment of real and nominal movements, adequate dynamics, and a credible identification strategy.

[PAGE]
# References

Agosin, Manuel R., and Ricardo Mayer. 2000. Foreign Investment in Developing Countries Does It Crowd in Domestic Investment? UNCTAD Discussion Paper 146. https://unctad.org/en/docs/dp_146.en.pdf

Borensztein, Eduardo, José De Gregorio, and Jong-Wha Lee. 1995. How Does Foreign Direct Investment Affect Economic Growth? NBER Working Paper 5057. https://doi.org/10.3386/w5057. Published in Journal of International Economics 45(1), 1998, 115–135.

Desai, Mihir A., C. Fritz Foley, and James R. Hines Jr. 2005. Foreign Direct Investment and the Domestic Capital Stock. NBER Working Paper 11075. https://doi.org/10.3386/w11075. Published in American Economic Review 95(2), 33–38.

Engle, Robert F., and C. W. J. Granger. 1987. Co Integration and Error Correction Representation Estimation and Testing. Econometrica 55(2), 251–276. https://doi.org/10.2307/1913236

Hamilton, James D. 2017. Why You Should Never Use the Hodrick Prescott Filter. NBER Working Paper 23429. https://doi.org/10.3386/w23429. Published in Review of Economics and Statistics 100(5), 2018, 831–843.

Hejazi, Walid, and Peter Pauly. 2002. Foreign Direct Investment and Domestic Capital Formation. Industry Canada Working Paper 36. https://ised-isde.canada.ca/site/economic-analysis-statistics/en/economic-research/archived-research/working-papers/working-paper-number-36-foreign-direct-investment-and-domestic-capital-formation

Javorcik, Beata Smarzynska. 2004. Does Foreign Direct Investment Increase the Productivity of Domestic Firms? In Search of Spillovers Through Backward Linkages. American Economic Review 94(3), 605–627. https://doi.org/10.1257/0002828041464605

Sambahamphe, Porokmi. 2019. The Effect of Foreign Direct Investment on Investment in Canada. ECON 310-01 undergraduate term paper. Archived original in the project repository.

Statistics Canada. n.d. Table 36-10-0222-01 Gross domestic product expenditure based provincial and territorial annual. https://doi.org/10.25318/3610022201-eng. Source metadata checked November 1, 2026; archived estimation values retained.

statsmodels developers. n.d. Documentation for adfuller, coint, GLSAR, regression HAC covariance estimation, and Breusch–Godfrey diagnostics. https://www.statsmodels.org/stable/. Software versions for the actual replication are recorded in results/environment.json.

Van Loo, Frances. 1977. The Effect of Foreign Direct Investment on Investment in Canada. Review of Economics and Statistics 59(4), 474–481. Historical reference used in the undergraduate project; the original study is not independently replicated in this extended working paper.

World Bank. n.d. World Development Indicators and Metadata Glossary. Series NE.DAB.TOTL.CD, BX.KLT.DINV.CD.WD, and PA.NUS.FCRF. https://databank.worldbank.org/metadataglossary/world-development-indicators/series/BX.KLT.DINV.CD.WD. Metadata checked November 1, 2026; archived estimation values retained.

[PAGE]
# Appendix A Variable construction and sample accounting

The investment outcome is business gross fixed capital formation, measured in current-price billions. The expenditure variable is gross national expenditure in the same currency. Slack is potential minus actual output valued at the nominal GDP price scale, as defined in equations (4)–(5). FDI is the annual net inflow, not its first difference except where explicitly indicated. Neither a negative slack value nor a fall in FDI is recoded to zero.

The main sample runs from 1981 to 2018 inclusive, producing 38 level observations. Taking first differences or shifting the long-run residual removes the first year, leaving 37 observations for the baseline ECM and the main change equations. The common-sample dynamic comparison also requires a lagged first difference, so it starts in 1983 and has 36 observations. The extended sample has 44 levels, 43 first-difference observations, and 42 common-sample dynamic observations. Effective ADF sample sizes depend additionally on their selected lags.

[TABLE sample]

The exchange-rate conversion is checked for each monetary variable and every year. Specifically, the absolute difference between the CAD value and the USD value multiplied by fx is required to be below a small floating-point tolerance. The overlapping years of the two archived files are checked for equality. These checks prevent unnoticed unit mismatches or inconsistent sample vintages from explaining the reported differences.

The long-run residual is estimated separately for each currency and sample endpoint. ECT is that residual shifted by one year. It is not an externally observed equilibrium gap. The fitted ECM uses contemporaneous first differences in expenditure, contemporaneous levels of U and FDI, and the lagged residual. The extended equations add an indicator equal to one in 2020 only.

# Appendix B Reproduction and research transparency

The accompanying replication package contains analysis.py, manuscript.md, the two archived input CSVs, generated results, figures, and environment information. From the package folder, install the stated dependencies and run python analysis.py. The program uses local data and does not download revised source values. It regenerates the numerical tables used to construct this extended working paper and records the environment and input-file hashes.

The baseline levels and AR(1) estimates use their fitted conventional covariance estimates. The change and error-correction models use HAC with three lags unless otherwise stated. Main-model comparisons use all available observations; the explicitly labeled common-sample dynamic table starts in 1983. Neither the latter coefficients nor their observation counts should be substituted silently into the 37-observation baseline table.

Leave-one-out checks are conditional coefficient-influence calculations. Differenced values, ECT, and slack are constructed before deleting each observation. The long-run regression and full-series filter are not rebuilt for every deletion. Because the remaining observations are not a consecutive annual sequence, the output does not report HAC or Breusch–Godfrey inference for those deletion exercises. The full coefficient list is retained in results/leave_one_out.csv.

The alternative ADF and cointegration configuration jointly changes the lag-search cap to three and the selection criterion to BIC. It is not a separate experiment isolating the effect of the information criterion alone. The manuscript reports reversals in the cointegration conclusions rather than selecting a configuration after observing the preferred result. No family-wise multiple-testing correction is applied; the extended specifications are exploratory diagnostics, not independent confirmatory discoveries.

AI assistance was used for coding, econometric discussion, source discovery, drafting, editing, and document preparation. The research question and the original undergraduate project are the author’s. The calculations in this package were executed on the archived data, but execution and internal consistency do not independently validate source measurement or causal assumptions. The author remains responsible for understanding the analysis, checking the cited sources, and deciding how the draft is used.

# Appendix C Reassessment of the original undergraduate project

The archived original is a Fall 2019 ECON 310-01 term paper. Its EViews ARMA maximum-likelihood table reports an FDI coefficient of 0.136900 and p = 0.0243, with 36 observations over a table-labeled 1981–2016 sample. The revised iterative GLSAR model reports 0.053241 with 37 effective observations from the reconstructed 1981–2018 dataset. These are different estimators applied to differently documented inputs, so the new coefficient is not presented as an exact replication failure or a formal historical trend.

The original interpreted an FDI coefficient below one as evidence of reduced investment by domestic firms. Section 3 explains why that conclusion requires an identity between financial inflows and foreign-owned fixed investment that these data do not satisfy. The extended working paper retains the original research interest while replacing that inference with a conditional-association interpretation.

The reconstruction also separates an autoregressive error correction from tests of integration and cointegration. An AR(1) disturbance model is not a correction for multicollinearity or a substitute for assessing trending series. The more cautious revised interpretation follows from the definitions and diagnostics, rather than from a preference for one software package over another.

The original PDF remains unchanged in the repository archive. This extended working paper and the shorter revised paper represent later research development. Keeping those outputs distinct preserves the historical record while allowing the current analysis to be assessed on its own documented assumptions, results, and remaining limitations.
