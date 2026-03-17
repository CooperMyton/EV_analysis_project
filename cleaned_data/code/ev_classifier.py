"""
ev_classifier.py

ML pipeline module for EV infrastructure analysis.
Predicts whether a county is over or underserved for EV charging.

Usage:
    from ev_classifier import build_features, train_models, evaluate_models

Or run directly:
    python ev_classifier.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings("ignore")


# Paths
ROOT     = Path(__file__).resolve().parent.parent
DATA_IN  = ROOT / "data_with_labels"
DATA_OUT = ROOT / "ev_features.csv"


# 1. Feature Engineering

def clean_numeric(series: pd.Series) -> pd.Series:
    """Strip commas and whitespace from a column and cast to float."""
    return series.astype(str).str.replace(",", "").str.strip().astype(float)


def build_features(input_path: Path = DATA_IN,
                output_path: Path = DATA_OUT,
                save: bool = True) -> pd.DataFrame:
    """
    Load data_with_labels, engineer ratio features, and save to a new file.
    Does NOT modify the original file.

    Returns:
        df (pd.DataFrame): feature-engineered dataframe
    """
    df = pd.read_csv(input_path)

    # Sanitise column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Clean numeric columns that may be stored as strings with commas
    df["pop_estimate"] = clean_numeric(df["pop_estimate"])
    df["daily_miles"]  = clean_numeric(df["daily_miles"])
    df["grand_total"]  = clean_numeric(df["grand_total"])
    df["total_kw"]     = clean_numeric(df["total_kw"])

    # Ratio features
    # For counties with total_kw=0, kw-based ratios are set to 0 (no chargers = genuinely underserved)
    # For counties with grand_total=0, ev-based ratios are set to 0
    df["kw_per_ev"]     = df["total_kw"]    / df["grand_total"].replace(0, np.nan)
    df["ev_per_capita"] = df["grand_total"] / df["pop_estimate"].replace(0, np.nan)
    df["kw_per_capita"] = df["total_kw"]    / df["pop_estimate"].replace(0, np.nan)
    df["miles_per_ev"]  = df["daily_miles"] / df["grand_total"].replace(0, np.nan)
    df["miles_per_kw"]  = df["daily_miles"] / df["total_kw"].replace(0, np.nan)

    # Fill NaNs caused by zero denominators with 0 rather than dropping the row
    for col in ["kw_per_ev", "kw_per_capita", "miles_per_kw"]:
        df[col] = df[col].fillna(0)

    # Only drop rows that are missing input data entirely
    df.dropna(subset=["ev_per_capita", "miles_per_ev"], inplace=True)

    if save:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Features saved to {output_path}")

    print(f"Feature matrix: {df.shape[0]} counties x {df.shape[1]} columns")
    return df


# 2. Model Definitions

def get_models() -> dict:
    """
    Returns a dict of model name -> sklearn Pipeline.
    Logistic Regression gets a scaler; tree-based models do not need one.
    """
    models = {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, random_state=42))
        ]),
        "Random Forest": Pipeline([
            ("clf", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))
        ]),
    }

    try:
        from xgboost import XGBClassifier
        models["XGBoost"] = Pipeline([
            ("clf", XGBClassifier(n_estimators=200, random_state=42,
                                eval_metric="logloss", verbosity=0))
        ])
    except ImportError:
        print("[!] xgboost not installed -- run: pip install xgboost")

    return models


# 3. Training and Evaluation

FEATURE_COLS = [
    "grand_total",
    "total_kw",
    "pop_estimate",
    "daily_miles",
    "kw_per_ev",
    "ev_per_capita",
    "kw_per_capita",
    "miles_per_ev",
    "miles_per_kw",
]


def train_models(df: pd.DataFrame,
                label_col: str = "cons_label",
                n_splits: int = 5) -> dict:
    """
    Train all models using stratified k-fold cross-validation.

    Args:
        df:        Feature-engineered dataframe from build_features()
        label_col: 'cons_label' or 'opt_label'
        n_splits:  Number of CV folds (default 5)

    Returns:
        results (dict): cross-val scores and fitted models keyed by model name
    """
    X = df[FEATURE_COLS].copy()
    y = LabelEncoder().fit_transform(df[label_col])

    cv      = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    scoring = ["accuracy", "f1_weighted", "roc_auc"]

    results = {}
    for name, model in get_models().items():
        scores = cross_validate(model, X, y, cv=cv, scoring=scoring, return_estimator=True)
        results[name] = {
            "accuracy":     scores["test_accuracy"].mean(),
            "accuracy_std": scores["test_accuracy"].std(),
            "f1":           scores["test_f1_weighted"].mean(),
            "roc_auc":      scores["test_roc_auc"].mean(),
            "estimators":   scores["estimator"],
        }
        print(
            f"  {name:<22} acc={results[name]['accuracy']:.3f}"
            f" +/- {results[name]['accuracy_std']:.3f}"
            f"  f1={results[name]['f1']:.3f}"
            f"  auc={results[name]['roc_auc']:.3f}"
        )

    return results


def evaluate_models(df: pd.DataFrame):
    """
    Run training on both cons_label and opt_label and print a comparison summary.
    Highlights counties where the two labels disagree (borderline cases).
    """
    print("\n" + "=" * 60)
    print("LABEL: cons_label (conservative charger utilisation)")
    print("=" * 60)
    cons_results = train_models(df, label_col="cons_label")

    print("\n" + "=" * 60)
    print("LABEL: opt_label (optimistic charger utilisation)")
    print("=" * 60)
    opt_results = train_models(df, label_col="opt_label")

    # Borderline counties
    borderline = df[df["opt_label"] != df["cons_label"]][["county", "opt_label", "cons_label"]]
    print("\n" + "=" * 60)
    print(f"BORDERLINE COUNTIES (opt vs cons disagree): {len(borderline)}")
    print("=" * 60)
    if len(borderline) > 0:
        print(borderline.to_string(index=False))
    else:
        print("  None -- labels fully agree across all counties.")

    # Summary table
    print("\n" + "=" * 60)
    print("SUMMARY TABLE")
    print("=" * 60)
    print(f"{'Model':<22} {'cons_acc':>9} {'cons_auc':>9} {'opt_acc':>8} {'opt_auc':>8}")
    print("-" * 60)
    for name in cons_results:
        print(
            f"{name:<22}"
            f" {cons_results[name]['accuracy']:>9.3f}"
            f" {cons_results[name]['roc_auc']:>9.3f}"
            f" {opt_results[name]['accuracy']:>8.3f}"
            f" {opt_results[name]['roc_auc']:>8.3f}"
        )

    return cons_results, opt_results


def feature_importance(df: pd.DataFrame, label_col: str = "cons_label") -> pd.DataFrame:
    """
    Fit a single Random Forest on all data and return feature importances.
    """
    X = df[FEATURE_COLS].copy()
    y = LabelEncoder().fit_transform(df[label_col])

    rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    rf.fit(X, y)

    importance_df = (
        pd.DataFrame({"feature": FEATURE_COLS, "importance": rf.feature_importances_})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    print("\n" + "=" * 40)
    print(f"FEATURE IMPORTANCES ({label_col})")
    print("=" * 40)
    for _, row in importance_df.iterrows():
        bar = "#" * int(row["importance"] * 40)
        print(f"  {row['feature']:<20} {row['importance']:.4f}  {bar}")

    return importance_df


if __name__ == "__main__":
    print("\n[1/3] Building features...")
    df = build_features()

    print("\n[2/3] Evaluating models...")
    cons_results, opt_results = evaluate_models(df)

    print("\n[3/3] Feature importances...")
    feature_importance(df, label_col="cons_label")

    print("\nDone.")