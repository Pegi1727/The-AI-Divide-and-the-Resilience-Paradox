"""
05_mediation_and_path_analysis.py
---------------------------------
Mediation Analysis Pipeline for:
The AI Divide and the Resilience Paradox

Evaluates:
- Path a: Bank_Barrier -> Motivation
- Path b: Motivation -> GPA (controlling for Bank_Barrier)
- Path c: Total effect (Bank_Barrier -> GPA)
- Path c': Direct effect (Bank_Barrier -> GPA controlling for Motivation)
- Sobel test & Bootstrap confidence intervals (5,000 resamples)
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

def run_mediation():
    df = pd.read_csv("/mnt/data/cleaned_dataset.csv")

    # 1. Total Effect (Path c)
    X = sm.add_constant(df[["Bank_Barrier"]])
    model_c = sm.OLS(df["GPA"], X).fit()
    c = model_c.params["Bank_Barrier"]
    p_c = model_c.pvalues["Bank_Barrier"]

    # 2. Path a (IV -> Mediator)
    model_a = sm.OLS(df["Motivation"], X).fit()
    a = model_a.params["Bank_Barrier"]
    se_a = model_a.bse["Bank_Barrier"]
    p_a = model_a.pvalues["Bank_Barrier"]

    # 3. Path b & Path c' (IV + Mediator -> DV)
    XM = sm.add_constant(df[["Bank_Barrier", "Motivation"]])
    model_bc = sm.OLS(df["GPA"], XM).fit()
    b = model_bc.params["Motivation"]
    se_b = model_bc.bse["Motivation"]
    p_b = model_bc.pvalues["Motivation"]
    c_prime = model_bc.params["Bank_Barrier"]
    p_c_prime = model_bc.pvalues["Bank_Barrier"]

    # 4. Indirect Effect
    indirect_effect = a * b

    # Sobel Test
    sobel_se = np.sqrt(b**2 * se_a**2 + a**2 * se_b**2)
    sobel_z = indirect_effect / sobel_se
    sobel_p = 2 * (1 - stats.norm.cdf(abs(sobel_z)))

    # 5. Non-parametric Bootstrapping (5,000 resamples)
    np.random.seed(42)
    n_boot = 5000
    boot_indirect = []
    n = len(df)

    for _ in range(n_boot):
        sample = df.sample(n=n, replace=True)
        m_a = sm.OLS(sample["Motivation"], sm.add_constant(sample[["Bank_Barrier"]])).fit()
        m_b = sm.OLS(sample["GPA"], sm.add_constant(sample[["Bank_Barrier", "Motivation"]])).fit()
        boot_indirect.append(m_a.params["Bank_Barrier"] * m_b.params["Motivation"])

    ci_lower = np.percentile(boot_indirect, 2.5)
    ci_upper = np.percentile(boot_indirect, 97.5)

    # Proportion mediated
    prop_mediated = indirect_effect / c if c != 0 else np.nan

    print("=" * 65)
    print("MEDIATION ANALYSIS SUMMARY (Bank_Barrier -> Motivation -> GPA)")
    print("=" * 65)
    print(f"Path a (Bank_Barrier -> Motivation):   Beta = {a:.4f}, SE = {se_a:.4f}, p = {p_a:.4e}")
    print(f"Path b (Motivation -> GPA):             Beta = {b:.4f}, SE = {se_b:.4f}, p = {p_b:.4e}")
    print(f"Total Effect (Path c):                  Beta = {c:.4f}, p = {p_c:.4e}")
    print(f"Direct Effect (Path c'):                Beta = {c_prime:.4f}, p = {p_c_prime:.4f}")
    print(f"Indirect Effect (a * b):                Estimate = {indirect_effect:.4f}")
    print(f"Sobel Test:                             Z = {sobel_z:.4f}, p = {sobel_p:.4e}")
    print(f"Bootstrap 95% CI (5,000 draws):        [{ci_lower:.4f}, {ci_upper:.4f}]")
    print(f"Proportion of Total Effect Mediated:    {prop_mediated * 100:.2f}%")
    print("=" * 65)

    if p_c_prime > 0.05 and ci_lower > 0:
        print("Interpretation: Full mediation confirmed (Direct effect becomes non-significant).")
    elif p_c_prime <= 0.05 and ci_lower > 0:
        print("Interpretation: Partial mediation confirmed.")
    print("=" * 65)

if __name__ == "__main__":
    run_mediation()
