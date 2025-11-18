"""
model_training.py

Train a Random Forest regression model to predict 3D printability
from generative design + slicer features.

Dataset: printable.csv
Author: Kaushik Teiledvara
"""

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

import matplotlib.pyplot as plt
import os


def load_data(csv_path: str = "printable.csv") -> pd.DataFrame:
    """
    Load the dataset from CSV.

    Parameters
    ----------
    csv_path : str
        Path to the printable.csv file.

    Returns
    -------
    df : pandas.DataFrame
        Loaded dataframe.
    """
    df = pd.read_csv(csv_path)
    return df


def prepare_features(df: pd.DataFrame):
    """
    Split dataframe into features X and target y.

    Target: print_success (0–1)

    Returns
    -------
    X : pandas.DataFrame
    y : pandas.Series
    """
    # Drop non-numeric / ID-like columns
    if "design_id" in df.columns:
        df = df.drop(columns=["design_id"])

    y = df["print_success"]
    X = df.drop(columns=["print_success"])

    return X, y


def train_model(X, y, random_state: int = 42):
    """
    Train a RandomForestRegressor on the dataset.

    Returns
    -------
    rf : fitted RandomForestRegressor
    X_train, X_test, y_train, y_test : train/test splits
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=random_state,
    )

    rf = RandomForestRegressor(
        n_estimators=200,
        random_state=random_state,
    )

    rf.fit(X_train, y_train)

    return rf, X_train, X_test, y_train, y_test


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance and print metrics.

    Returns
    -------
    r2 : float
    mae : float
    """
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print("=== Model Evaluation ===")
    print(f"R^2 score:           {r2:.3f}")
    print(f"Mean Absolute Error:  {mae:.3f}")

    return r2, mae, y_pred


def plot_feature_importance(model, feature_names, output_dir=".", filename="feature_importance.png"):
    """
    Save a horizontal bar chart of feature importances.
    """
    importances = model.feature_importances_
    fi_df = pd.DataFrame({"feature": feature_names, "importance": importances})
    fi_df = fi_df.sort_values(by="importance", ascending=False)

    plt.figure(figsize=(8, 6))
    plt.barh(fi_df["feature"], fi_df["importance"])
    plt.xlabel("Importance")
    plt.title("Random Forest Feature Importance")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved feature importance plot to: {output_path}")


def plot_actual_vs_pred(y_test, y_pred, output_dir=".", filename="actual_vs_pred.png"):
    """
    Save scatter plot of actual vs predicted print_success.
    """
    plt.figure(figsize=(5, 5))
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual print_success")
    plt.ylabel("Predicted print_success")
    plt.title("Random Forest: Actual vs Predicted")
    plt.grid(True)
    plt.tight_layout()

    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved actual vs predicted plot to: {output_path}")


def main():
    # 1. Load data
    df = load_data("printable.csv")

    # 2. Prepare features and labels
    X, y = prepare_features(df)

    # 3. Train model
    model, X_train, X_test, y_train, y_test = train_model(X, y)

    # 4. Evaluate
    r2, mae, y_pred = evaluate_model(model, X_test, y_test)

    # 5. Generate plots (saved as PNGs in repo root)
    plot_feature_importance(model, X.columns)
    plot_actual_vs_pred(y_test, y_pred)


if __name__ == "__main__":
    main()
