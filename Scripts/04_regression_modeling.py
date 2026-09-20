"""
04_regression_modeling.py
OLS bivariate & multiple regression, diagnostics, robust regression (RLM).
Reads /mnt/data/cleaned_dataset.csv.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson, jarque_bera

CSV = "/mnt/data/cleaned_dataset.csv"
PREDICTORS_MULT = ["Access_Plus", "Bank_Barrier", "Resilience", "Motivation"]


def fit_ols(df, y, xs, label):
    X = sm.add_constant(df[xs].astype(float))
    model = sm.OLS(df[y].astype(float), X).fit()
    print(f"\n=== OLS: {label} ===\n{model.summary()}")
    return model


def diagnostics(model, df):
    infl = model.get_influence()
    cooks = infl.cooks_distance[0]
    bp_lm, bp_p, bp_f, bp_fp = het_breuschpagan(model.resid, model.model.exog)
    jb, jbp, skew, kurt = jarque_bera(model.resid)
    dw = durbin_watson(model.resid)
    diag = pd.DataFrame({
        "Statistic": {"BreuschPagan_LM": bp_lm, "BreuschPagan_p": bp_p,
                      "JarqueBera_JB": jb, "JarqueBera_p": jbp,
                      "DurbinWatson": dw,
                      "Max_CooksD": cooks.max(),
                      "N_CooksD_gt_4_over_n": int((cooks > 4 / len(df)).sum())}
    })
    print("\n=== DIAGNOSTICS ===\n", diag.to_string())
    print("Guide: BP p>0.05 -> homoskedastic; JB p>0.05 -> normal residuals;")
    print("DW~2 -> no autocorrelation; Cook\'s D > 4/n -> influential observation.")
    return diag, cooks


def robust_comparison(df, y, xs):
    X = sm.add_constant(df[xs].astype(float))
    yv = df[y].astype(float)
    out = {"OLS": sm.OLS(yv, X).fit().params}
    for name, norm in [("RLM_HuberT", sm.robust.norms.HuberT()),
                       ("RLM_TukeyBiweight", sm.robust.norms.TukeyBiweight())]:
        rlm = sm.RLM(yv, X, M=norm).fit()
        out[name] = rlm.params
        print(f"\n=== {name} ===\n{rlm.summary()}")
    comp = pd.DataFrame(out)
    print("\n=== COEFFICIENT COMPARISON (OLS vs Robust) ===\n", comp.to_string())
    return comp


def main():
    df = pd.read_csv(CSV)
    m1 = fit_ols(df, "GPA", ["Access_Plus"], "Bivariate: GPA ~ Access_Plus")
    m2 = fit_ols(df, "GPA", PREDICTORS_MULT,
                 "Multiple: GPA ~ Access_Plus + Bank_Barrier + Resilience + Motivation")
    diag, cooks = diagnostics(m2, df)
    comp = robust_comparison(df, "GPA", PREDICTORS_MULT)
    with open("/mnt/data/regression_results.txt", "w") as f:
        f.write("=== BIVARIATE OLS: GPA ~ Access_Plus ===\n%s\n\n" % m1.summary())
        f.write("=== MULTIPLE OLS ===\n%s\n\n" % m2.summary())
        f.write("=== DIAGNOSTICS ===\n%s\n\n" % diag.to_string())
        f.write("=== ROBUST COMPARISON ===\n%s\n" % comp.to_string())
    np.save("/mnt/data/cooks_distance.npy", cooks)
    print("\nExported: regression_results.txt, cooks_distance.npy")


if __name__ == "__main__":
    main()
