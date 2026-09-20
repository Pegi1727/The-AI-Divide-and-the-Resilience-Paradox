"""
06_publication_plots.py
-----------------------
Generates high-resolution (300 DPI) publication-grade figures:
1. Correlation Matrix Heatmap
2. GPA Distribution across AI Access Tiers (Violin & Boxplot)
3. Scatterplots with Linear Regressions (GPA vs Motivation, GPA vs Access_Plus)
4. Path Diagram of Mediation Analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Styling configuration
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["xtick.labelsize"] = 9
plt.rcParams["ytick.labelsize"] = 9
plt.rcParams["figure.dpi"] = 300

def generate_plots():
    df = pd.read_csv("/mnt/data/cleaned_dataset.csv")

    # 1. Correlation Matrix Heatmap
    num_cols = ["Access_Plus", "Bank_Barrier", "Resilience", "Motivation", "GPA"]
    corr = df[num_cols].corr(method="pearson")

    fig, ax = plt.subplots(figsize=(7, 6))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.heatmap(
        corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
        annot=True, fmt=".2f", square=True, linewidths=.8,
        cbar_kws={"shrink": .8, "label": "Pearson Correlation (r)"}, ax=ax
    )
    ax.set_title("Figure 1: Inter-variable Correlation Matrix", pad=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig("/mnt/data/fig1_correlation_matrix.png")
    plt.close()

    # 2. Violin & Boxplot: GPA by Access Tiers
    fig, ax = plt.subplots(figsize=(6, 5))
    palette = ["#4C72B0", "#DD8452"]
    sns.violinplot(x="Access_Tier", y="GPA", data=df, hue="Access_Tier", palette=palette, inner=None, alpha=0.4, ax=ax, legend=False)
    sns.boxplot(x="Access_Tier", y="GPA", data=df, hue="Access_Tier", palette=palette, width=0.25, showcaps=True,
                boxprops={"zorder": 2}, ax=ax, legend=False)
    sns.stripplot(x="Access_Tier", y="GPA", data=df, color="black", alpha=0.6, jitter=0.15, size=5, ax=ax)
    ax.set_title("Figure 2: GPA Distribution by AI Access Tier", pad=12, fontweight="bold")
    ax.set_xlabel("AI Access Status", labelpad=8)
    ax.set_ylabel("Grade Point Average (GPA)", labelpad=8)
    plt.tight_layout()
    plt.savefig("/mnt/data/fig2_access_vs_gpa_distribution.png")
    plt.close()

    # 3. Dual Regression Scatterplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

    # Plot A: Motivation vs GPA
    sns.regplot(x="Motivation", y="GPA", data=df, ax=ax1,
                color="#2ca02c", scatter_kws={"alpha": 0.6}, line_kws={"linewidth": 2})
    ax1.set_title("A: Academic Motivation vs GPA", fontweight="bold")
    ax1.set_xlabel("Motivation Score")
    ax1.set_ylabel("GPA")

    # Plot B: Access_Plus vs GPA
    sns.regplot(x="Access_Plus", y="GPA", data=df, ax=ax2,
                color="#d62728", scatter_kws={"alpha": 0.6}, line_kws={"linewidth": 2})
    ax2.set_title("B: Premium AI Access vs GPA", fontweight="bold")
    ax2.set_xlabel("Access Plus (Hours / Usage Intensity)")
    ax2.set_ylabel("GPA")

    plt.suptitle("Figure 3: Key Bivariate Associations with Academic Performance", y=1.02, fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig("/mnt/data/fig3_regression_slopes.png")
    plt.close()

    print("All figures successfully created at 300 DPI.")

if __name__ == "__main__":
    generate_plots()
