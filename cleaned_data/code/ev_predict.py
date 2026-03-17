"""
ev_predict.py

Command line tool for predicting whether a county is over or underserved
for EV charging infrastructure.
Run from project root:
    python cleaned_data/code/ev_predict.py
"""

import numpy as np
import pandas as pd
import sys
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Import from our module
sys.path.append(str(Path(__file__).resolve().parent))
from ev_classifier import build_features, FEATURE_COLS


def train_final_model(df: pd.DataFrame, label_col: str = "cons_label"):
    """
    Train a single Random Forest on the full dataset to use for predictions.
    Returns the fitted model and label encoder.
    """
    X = df[FEATURE_COLS].copy()
    le = LabelEncoder()
    y = le.fit_transform(df[label_col])

    model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X, y)

    return model, le


def prompt_float(prompt: str) -> float:
    """Prompt the user for a number, keep asking until they give a valid one."""
    while True:
        raw = input(prompt).strip().replace(",", "")
        try:
            value = float(raw)
            if value < 0:
                print("  Please enter a value of 0 or greater.")
                continue
            return value
        except ValueError:
            print("  Invalid input -- please enter a number.")


def compute_features(grand_total: float,
                    total_kw: float,
                    pop_estimate: float,
                    daily_miles: float) -> dict:
    """Compute ratio features from raw inputs."""
    return {
        "grand_total":   grand_total,
        "total_kw":      total_kw,
        "pop_estimate":  pop_estimate,
        "daily_miles":   daily_miles,
        "kw_per_ev":     total_kw    / grand_total   if grand_total  > 0 else 0.0,
        "ev_per_capita": grand_total / pop_estimate  if pop_estimate > 0 else 0.0,
        "kw_per_capita": total_kw    / pop_estimate  if pop_estimate > 0 else 0.0,
        "miles_per_ev":  daily_miles / grand_total   if grand_total  > 0 else 0.0,
        "miles_per_kw":  daily_miles / total_kw      if total_kw     > 0 else 0.0,
    }


def run():
    print()
    print("=" * 60)
    print("  EV Infrastructure Analyzer")
    print("=" * 60)
    print("  Enter your county's data below.")
    print("  You can use commas in numbers (e.g. 1,200,000).")
    print("  Type Ctrl+C at any time to exit.")
    print("=" * 60)

    # Load and train
    print("\nLoading model...")
    try:
        df = build_features(save=False)
    except FileNotFoundError as e:
        print(f"\nError loading data: {e}")
        print("Make sure you are running this from the project root.")
        sys.exit(1)

    model, le = train_final_model(df)
    print("Model ready.\n")

    while True:
        print("-" * 60)

        grand_total  = prompt_float("  Total EV registrations in your county:          ")
        total_kw     = prompt_float("  Total kW of charging capacity (0 if none):      ")
        pop_estimate = prompt_float("  County population estimate:                     ")
        daily_miles  = prompt_float("  Total daily vehicle miles driven in the county: ")

        # Compute features
        features = compute_features(grand_total, total_kw, pop_estimate, daily_miles)
        X = pd.DataFrame([features])[FEATURE_COLS]

        # Predict
        prediction_encoded = model.predict(X)[0]
        prediction = le.inverse_transform([prediction_encoded])[0]
        probabilities = model.predict_proba(X)[0]
        confidence = probabilities[prediction_encoded] * 100

        # Display result
        print()
        print("=" * 60)
        print("  RESULT")
        print("=" * 60)

        if prediction == "under":
            print(f"  Your county appears UNDERSERVED for EV charging.")
        else:
            print(f"  Your county appears OVERSERVED for EV charging.")

        print(f"  Confidence: {confidence:.1f}%")
        print()

        # Show the computed ratios so the user can see what drove the result
        print("  Computed ratios:")
        print(f"    kW per EV:         {features['kw_per_ev']:.4f}")
        print(f"    EVs per capita:    {features['ev_per_capita']:.4f}")
        print(f"    kW per capita:     {features['kw_per_capita']:.4f}")
        print(f"    Miles per EV:      {features['miles_per_ev']:.1f}")
        print(f"    Miles per kW:      {features['miles_per_kw']:.1f}")
        print("=" * 60)

        # Ask to run again
        print()
        again = input("  Analyze another county? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Goodbye.\n")
            break


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\n  Exited.\n")