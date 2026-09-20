"""
02_descriptive_and_normality.py
Parametric & non-parametric descriptives, normality tests, group comparisons.
Reads /mnt/data/cleaned_dataset.csv, exports summary tables.
"""
import pandas as pd
import numpy as np
from scipy import stats

CSV = "/mnt/data/cleaned_dataset.csv"
VARS = ["Access_Plus", "Bank_Barrier", "Resilience", "Motivation", "GPA"]


def descriptive_table(df):
    rows = []
    for v in VARS:
        x = df[v].dropna()
        rows.append({
            "Variable": v, "N": len(x), "Mean": x.mean(), "SD": x.std(ddof=1),
            "Median": x.median(), "IQR": stats.iqr(x),
            "Min": x.min(), "Max": x.max(),
            "Skewness": stats.skew(x, bias=False), "Kurtosis": stats.kurtosis(x, bias=False),
        })
    return pd.DataFrame(rows).set_index("Variable")


def normality_table(df):
    rows = []
    for v in VARS:
        x = df[v].dropna()
        w, pw = stats.shapiro(x)
        dag, pdag = stats.normaltest(x)  # D'Agostino-Pearson K^2
        rows.append({"Variable": v, "Shapiro_W": w, "Shapiro_p": pw,
                     "DAgostino_K2": dag, "DAgostino_p": pdag,
                     "Normal_05": bool((pw > .05) and (pdag > .05))})
    return pd.DataFrame(rows).set_index("Variable")


def group_comparisons(df, group_col="Access_Group"):
    rows = []
    levels = sorted(df[group_col].dropna().unique())
    for v in VARS:
        a = df.loc[df[group_col] == levels[0], v].dropna()
        b = df.loc[df[group_col] == levels[1], v].dropna()
        t, pt = stats.ttest_ind(a, b, equal_var=False)  # Welch
        u, pu = stats.mannwhitneyu(a, b, alternative="two-sided")
        sp = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
        d = (a.mean() - b.mean()) / sp if sp > 0 else np.nan
        rbc = 1 - 2 * u / (len(a) * len(b))
        rows.append({"Variable": v,
                     f"{levels[0]}_M": a.mean(), f"{levels[1]}_M": b.mean(),
                     "Welch_t": t, "t_p": pt, "MannWhitney_U": u, "U_p": pu,
                     "Cohens_d": d, "Rank_biserial_r": rbc})
    return pd.DataFrame(rows).set_index("Variable")


def main():
    df = pd.read_csv(CSV)
    desc = descriptive_table(df)
    norm = normality_table(df)
    grp = group_comparisons(df)
    pd.set_option("display.float_format", lambda v: f"{v:.4f}")
    print("\n=== DESCRIPTIVES ===\n", desc.to_string())
    print("\n=== NORMALITY ===\n", norm.to_string())
    print("\n=== GROUP COMPARISON (Access_Group) ===\n", grp.to_string())
    desc.to_csv("/mnt/data/table1_descriptives.csv")
    norm.to_csv("/mnt/data/table2_normality.csv")
    grp.to_csv("/mnt/data/table3_group_comparisons.csv")
    print("\nExported: table1_descriptives.csv, table2_normality.csv, table3_group_comparisons.csv")


if __name__ == "__main__":
    main()
