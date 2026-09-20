<p align="center">
  <h1 align="center">The AI Divide and the Resilience Paradox</h1>
  <p align="center">
    <strong>Digital Sanctions, Adaptive Agency, and Academic Tenacity among Iranian Scholars</strong>
  </p>
  <p align="center">
    <a href="https://doi.org/10.5281/zenodo.22862815"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.22862815.svg" alt="DOI"></a>
    <a href="https://github.com/Pegi1727/The-AI-Divide-and-the-Resilience-Paradox/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.10+-yellow.svg" alt="Python 3.10+"></a>
    <a href="https://www.r-project.org/"><img src="https://img.shields.io/badge/R-4.3+-blue.svg" alt="R 4.3+"></a>
    <a href="https://sqlite.org/"><img src="https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-lightgrey.svg" alt="SQL"></a>
    <a href="https://github.com/Pegi1727/The-AI-Divide-and-the-Resilience-Paradox/actions"><img src="https://img.shields.io/badge/CI%2FCD-Passing-brightgreen.svg" alt="CI/CD"></a>
  </p>
</p>

---

## 🖼️ Visual Evidence & Figures

### Graphical Abstract
<p align="center">
  <img src="Figures/graphical%20abstract.png" alt="Graphical Abstract" width="920"/>
</p>

### Figure 1: Methodological Architecture & Research Pipeline
<p align="center">
  <img src="Figures/figure1_methodology.png" alt="Figure 1: Research Methodology Pipeline" width="880"/>
</p>

### Empirical Distributions & Correlation Structure
<table align="center">
  <tr>
    <td align="center"><strong>Figure 2: Empirical Distributions & Group Spreads</strong></td>
    <td align="center"><strong>Figure 3: Correlation Matrix (Pearson & Spearman)</strong></td>
  </tr>
  <tr>
    <td><img src="Figures/figure2_distributions.png" alt="Figure 2: Distributions" width="440"/></td>
    <td><img src="Figures/figure3_correlation_matrix.png" alt="Figure 3: Correlation Matrix" width="440"/></td>
  </tr>
</table>

### Model Validation & The Resilience Paradox
<table align="center">
  <tr>
    <td align="center"><strong>Figure 4: The Empirical Resilience Paradox</strong></td>
    <td align="center"><strong>Figure 5: Regression Modeling & Diagnostics</strong></td>
  </tr>
  <tr>
    <td><img src="Figures/figure4_resilience_paradox.png" alt="Figure 4: Resilience Paradox" width="440"/></td>
    <td><img src="Figures/figure5_regression_model.png" alt="Figure 5: Regression Model" width="440"/></td>
  </tr>
</table>

---

## 🏷️ Persistent Identifier (DOI) & Citation

This research archive is permanently preserved on Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22862815.svg)](https://doi.org/10.5281/zenodo.22862815)  
*(Direct Resolver: `https://doi.org/10.5281/zenodo.22862815`)*

### APA 7th Edition
> Merrikhi, P. (2026). *Replication Package and Empirical Dataset for "The AI Divide and the Resilience Paradox: Digital Sanctions, Adaptive Agency, and Academic Tenacity among Iranian Scholars"* (Version v1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.22862815

### BibTeX
```bibtex
@misc{merrikhi2026aidivide,
  author       = {Merrikhi, Pegah},
  title        = {{Replication Package and Empirical Dataset for "The AI Divide 
and the Resilience Paradox: Digital Sanctions, Adaptive Agency, 
and Academic Tenacity among Iranian Scholars"}},
  month        = sep,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0.0},
  doi          = {10.5281/zenodo.22862815
  ---
📈 Empirical Results & Statistical Tables
All findings are derived from 
𝑁
=
60
N=60
 Iranian academic scholars across verified institutional tiers.

1. Descriptive Statistics of Core Variables

Variable	Construct Role	Mean	SD	Min	Max	Skewness	Kurtosis
Access_Plus	AI Subscription / Access Tier (1–5)	3.42	1.83	1.00	5.00	-0.53	-1.54
Bank_Barrier	Payment / Digital Sanction Friction	3.08	1.36	1.00	5.00	0.22	-1.41
Resilience	Academic Resilience & Tenacity	3.37	1.07	2.00	5.00	0.23	-1.18
Motivation	Compensatory Cognitive Drive	3.00	1.21	1.00	5.00	0.12	-1.14
GPA	Academic Performance Metric	87.90	4.96	80.00	99.00	0.40	-0.66
2. Bivariate Pearson Correlation Matrix (
𝑁
=
60
N=60
)

Construct	Access_Plus	Bank_Barrier	Resilience	Motivation	GPA
Access_Plus	1.000	-0.902***	-0.841***	-0.852***	-0.809***
Bank_Barrier	-	1.000	0.814***	0.854***	+0.834***
Resilience	-	-	1.000	0.826***	+0.803***
Motivation	-	-	-	1.000	+0.880***
GPA	-	-	-	-	1.000
*p < .05, **p < .01, ***p < .001 (Two-tailed).

3. Access Tier Comparisons (Restricted Tier 1 vs. Seamless Tier 5)
A Welch’s two-sample 
𝑡
t
-test indicates that scholars facing severe infrastructural bottlenecks significantly out-performed their seamless-access counterparts:


Metric	Restricted Access (
𝑛
1
=
21
n 
1
​
 =21
)	Seamless Access (
𝑛
2
=
28
n 
2
​
 =28
)	
𝑡
t
-statistic	
𝑝
p
-value	Cohen’s 
𝑑
d
Mean GPA	93.52 (
±
2.91
±2.91
)	85.00 (
±
2.60
±2.60
)	10.62	
3.1
×
10
−
13
3.1×10 
−13
 
3.09 (Very Large)
Mean Resilience	4.52 (
±
0.51
±0.51
)	2.50 (
±
0.51
±0.51
)	13.68	
<
10
−
15
<10 
−15
 
3.96
Mean Motivation	4.33 (
±
0.48
±0.48
)	2.00 (
±
0.00
±0.00
)	22.25	
<
10
−
15
<10 
−15
 
6.86
4. OLS Multiple Linear Regression Model
Dependent Variable: Academic Performance (GPA)
Overall Model Fit: 
𝑅
2
=
0.810
R 
2
 =0.810
, 
Adjusted 
𝑅
2
=
0.796
Adjusted R 
2
 =0.796
, 
𝐹
(
4
,
55
)
=
58.64
F(4,55)=58.64
, 
𝑝
=
2.98
×
10
−
19
p=2.98×10 
−19
 

Predictor	
𝛽
β
 (Coeff)	Std. Error	
𝑡
t
-value	
𝑝
p
-value	95% Conf. Interval
Intercept	76.541	3.218	23.785	
<
.001
<.001
[70.092, 82.990]
Access_Plus	-0.596	0.384	-1.552	.126	[-1.365, 0.173]
Bank_Barrier	0.138	0.597	0.231	.818	[-1.058, 1.334]
Resilience	0.512	0.544	0.941	.350	[-0.578, 1.602]
Motivation	2.408	0.589	4.088	
<
.001
<.001
[1.228, 3.588]
Diagnostic Note on Multicollinearity: The structural coupling of digital barriers and compensatory agency induces multicollinearity among predictors, establishing Motivation as the proximate engine through which resilience and environmental friction manifest as scholastic excellence.

5. Path Analysis & Mediation Breakdown
Mediation Pathway: 
Bank_Barrier
⟶
Compensatory Motivation
⟶
GPA
Bank_Barrier⟶Compensatory Motivation⟶GPA
Total Effect (
𝑐
c
): 
3.062
3.062
 (
𝑝
<
.001
p<.001
)
Direct Effect (
𝑐
′
c 
′
 
): 
0.972
0.972
 (
𝑝
=
.034
p=.034
)
Indirect Mediation Effect (
𝑎
×
𝑏
a×b
): 
2.090
2.090
 (
𝑝
<
.001
p<.001
)
Mediation Ratio: 
68.25
%
68.25%
 of the barrier effect on academic excellence is channeled via adaptive compensatory motivation.
💡 Conclusion & Theoretical Implications
The Resilience Paradox Is Real:Counter to conventional technological determinism, frictionless AI adoption does not guarantee superior scholarly outcomes. Unhindered access often leads to cognitive offloading and superficial engagement.
Adaptive Agency as a Compensatory Catalyst:Scholars navigating digital sanctions develop complex workarounds, cognitive tenacity, and higher intrinsic motivation, enabling them to out-perform unconstrained peers in rigorous evaluation metrics (
𝑑
=
3.09
d=3.09
).
Policy & Global AI Ethics:Geopolitical digital exclusions remain fundamentally unjust and counterproductive to open science; however, global educational institutions must recognize that cultivating grit, metacognitive tenacity, and critical AI engagement is far more decisive for academic mastery than passive platform access alone.
---
🎯 Executive Summary & Overview
This repository constitutes the complete reproducibility package, curated empirical dataset, and analytical pipeline for the study:

“The AI Divide and the Resilience Paradox: Digital Sanctions, Adaptive Agency, and Academic Tenacity among Iranian Scholars.”

The research examines a counter-intuitive sociotechnical phenomenon: scholars subjected to geopolitical digital exclusions, tiered access restrictions (e.g., restricted institutional access to frontier LLMs), and international payment frictions demonstrate counter-intuitively superior academic tenacity and achievement (GPA) compared to their unrestricted peers, mediated by compensatory agency and intrinsic motivation.
---
📂 Repository Structure
text
  url          = {https://doi.org/10.5281/zenodo.22862815}
}
