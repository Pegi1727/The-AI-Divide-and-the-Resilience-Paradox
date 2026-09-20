"""
03_correlation_and_collinearity.py
Pearson & Spearman correlation matrices with exact p-values,
VIF and Condition Index collinearity diagnostics, ranked pairs.
Reads /mnt/data/cleaned_dataset.csv.
"""
import itertools
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

CSV = "/mnt/data/cleaned_dataset.csv"
VARS = ["Access_Plus", "Bank_Barrier", "Resilience", "Motivation", "GPA"]


def _pval_matrix(df, func):
    n = len(VARS)
    p = pd.DataFrame(np.ones((n, n)), index=VARS, columns=VARS)
    for a, b in itertools.combinations(VARS, 2):
        x, y = df[a].dropna(), df[b].dropna()
        idx = df[[a, b]].dropna().index
        r, pv = func(df.loc[idx, a], df.loc[idx, b])
        p.loc[a, b] = p.loc[b, a] = pv
    return p


def pearson_spearman(df):
    pr = df[VARS].corr(method="pearson")
    sp = df[VARS].corr(method="spearman")
    pp = _pval_matrix(df, lambda a, b: stats.pearsonr(a, b)[:2])
    spp = _pval_matrix(df, lambda a, b: stats.spearmanr(a, b))
    return pr, pp, sp, spp


def collinearity(df):
    X = add_constant(df[VARS].astype(float))
    vif = pd.Series([variance_inflation_factor(X.values, i) for i in range(1, X.shape[1])],
                    index=VARS, name="VIF")
    corr = df[VARS].astype(float).corr().values
    eigvals = np.linalg.eigvalsh(corr)[::-1]
    cond_index = np.sqrt(eigvals[0] / eigvals)
    cond = pd.Series(cond_index, index=[f"Component_{i+1}" for i in range(len(eigvals))], name="Condition_Index")
    return vif, cond, eigvals


def ranked_pairs(r, p):
    rows = []
    for a, b in itertools.combinations(VARS, 2):
        rows.append({"Pair": f"{a} ~ {b}", "r": r.loc[a, b], "p": p.loc[a, b]})
    return pd.DataFrame(rows).sort_values("r", ascending=False, key=abs).reset_index(drop=True)


def interpret(r):
    a = abs(r)
    if a >= .7: return "Strong"
    if a >= .4: return "Moderate"
    if a >= .2: return "Weak"
    return "Negligible"


def main():
    df = pd.read_csv(CSV)
    pr, pp, sp, spp = pearson_spearman(df)
    vif, cond, eig = collinearity(df)
    pd.set_option("display.float_format", lambda v: f"{v:.4f}")
    print("\n=== PEARSON r ===\n", pr.to_string())
    print("\n=== PEARSON p-values ===\n", pp.to_string())
    print("\n=== SPEARMAN rho ===\n", sp.to_string())
    print("\n=== SPEARMAN p-values ===\n", spp.to_string())
    print("\n=== VIF ===\n", vif.to_string())
    print("\n=== CONDITION INDICES ===\n", cond.to_string())
    print("\nMax VIF: %.3f | Max Condition Index: %.3f" % (vif.max(), cond.max()))
    ranked = ranked_pairs(pr, pp)
    ranked["Strength"] = ranked["r"].apply(interpret)
    print("\n=== RANKED PEARSON PAIRS ===\n", ranked.to_string(index=False))
    pr.to_csv("/mnt/data/corr_pearson.csv"); pp.to_csv("/mnt/data/corr_pearson_p.csv")
    sp.to_csv("/mnt/data/corr_spearman.csv"); spp.to_csv("/mnt/data/corr_spearman_p.csv")
    vif.to_csv("/mnt/data/collinearity_vif.csv"); cond.to_csv("/mnt/data/collinearity_condition.csv")
    ranked.to_csv("/mnt/data/corr_ranked_pairs.csv", index=False)
    print("\nExported correlation & collinearity CSVs.")


if __name__ == "__main__":
    main()
