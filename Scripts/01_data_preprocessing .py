"""
01_data_preprocessing.py
Load, validate, clean and feature-engineer the AI Resilience empirical dataset.
Outputs: /mnt/data/cleaned_dataset.csv
"""
import pandas as pd
import numpy as np

INPUT = "/mnt/data/AI_Resilience_Empirical_Dataset.xlsx"
OUTPUT = "/mnt/data/cleaned_dataset.csv"

EXPECTED_COLS = ["ID", "Access_Plus", "Bank_Barrier", "Resilience", "Motivation", "GPA", "Status"]
VALID_RANGES = {
    "Access_Plus": (1, 5), "Bank_Barrier": (1, 5), "Resilience": (1, 5),
    "Motivation": (1, 5), "GPA": (0, 100), "Status": (0, 10),
}


def load_data(path=INPUT):
    df = pd.read_excel(path)
    print(f"Loaded {df.shape[0]} rows x {df.shape[1]} cols from {path}")
    return df


def validate(df):
    issues = []
    missing_cols = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing_cols:
        issues.append(f"Missing columns: {missing_cols}")
    print("\nDtypes:\n", df.dtypes)
    print("\nMissing values:\n", df.isna().sum())
    for col, (lo, hi) in VALID_RANGES.items():
        if col in df.columns:
            out = df[(df[col] < lo) | (df[col] > hi)]
            if len(out):
                issues.append(f"{col}: {len(out)} out-of-range values")
            if not pd.api.types.is_numeric_dtype(df[col]):
                issues.append(f"{col}: not numeric")
    if "ID" in df.columns and df.duplicated(subset=["ID"]).any():
        issues.append("Duplicate IDs found")
    print("\nValidation issues:", issues if issues else "NONE - dataset passes all checks")
    return issues


def engineer(df):
    df = df.copy()
    for c in ["Access_Plus", "Bank_Barrier", "Resilience", "Motivation", "GPA"]:
        df[f"{c}_c"] = df[c] - df[c].mean()
    access_median = df["Access_Plus"].median()
    df["Access_Group"] = np.where(df["Access_Plus"] > access_median, "High", "Low")
    df["Resilience_Group"] = np.where(df["Resilience"] > df["Resilience"].median(), "High", "Low")
    df["Barrier_Group"] = np.where(df["Bank_Barrier"] > df["Bank_Barrier"].median(), "High_Barrier", "Low_Barrier")
    print("\nAccess_Group counts:\n", df["Access_Group"].value_counts().to_string())
    return df


def main():
    df = load_data()
    validate(df)
    df = engineer(df)
    df.to_csv(OUTPUT, index=False)
    print(f"\nSaved cleaned dataset -> {OUTPUT}  ({df.shape[0]} rows, {df.shape[1]} cols)")


if __name__ == "__main__":
    main()
