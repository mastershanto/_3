#!/usr/bin/env python3
"""
linear_regrassion.py

Simple linear regression project using scikit-learn and the California Housing dataset.

Usage:
  python linear_regrassion.py --mode train
  python linear_regrassion.py --mode predict --n-samples 5

This script supports:
 - training a linear regression model
 - saving the model and scaler
 - making predictions using the saved model
 - plotting results (predicted vs actual, residuals)

The helper `scripts/setup_venv.sh` sets up a venv with Python 3.14 and installs requirements.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Optional

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(as_frame: bool = True) -> tuple[pd.DataFrame, pd.Series]:
    ds = fetch_california_housing(as_frame=as_frame)
    X = ds.data
    y = ds.target
    return X, y


def train_model(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42, model_path: Path | str = "models/linear_regression.joblib") -> None:
    os.makedirs(Path(model_path).parent, exist_ok=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    predictions = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("Training completed")
    print(f"MSE: {mse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"R2 : {r2:.4f}")

    # Save model and scaler
    joblib.dump(model, model_path)
    joblib.dump(scaler, str(Path(model_path).parent / "scaler.joblib"))
    print(f"Model saved to {model_path}")

    # Save a small test CSV for demonstration
    test_df = X_test.copy()
    test_df["target"] = y_test.values
    test_df["predicted"] = predictions
    test_df.to_csv(str(Path(model_path).parent / "test_results.csv"), index=False)
    print("Saved test results to models/test_results.csv")

    return model, scaler, X_test, y_test, predictions


def plot_results(y_true: np.ndarray, y_pred: np.ndarray, save_path: Path | None = None) -> None:
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].scatter(y_true, y_pred, alpha=0.5)
    axs[0].set_title("Predicted vs Actual")
    axs[0].set_xlabel("Actual")
    axs[0].set_ylabel("Predicted")
    minv = min(y_true.min(), y_pred.min())
    maxv = max(y_true.max(), y_pred.max())
    axs[0].plot([minv, maxv], [minv, maxv], color="red", linestyle="--")

    residuals = y_true - y_pred
    axs[1].hist(residuals, bins=30)
    axs[1].set_title("Residual histogram")
    axs[1].set_xlabel("Residual")
    axs[1].set_ylabel("Count")

    plt.tight_layout()
    if save_path:
        plt.savefig(str(save_path))
        print(f"Saved plot to {save_path}")
    else:
        plt.show()


def predict(n_samples: Optional[int] = None, model_path: str = "models/linear_regression.joblib", random_state: int = 42):
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model file not found. Run training mode first.")
    model = joblib.load(model_path)
    scaler = joblib.load(os.path.join(Path(model_path).parent, "scaler.joblib"))

    X, y = load_data()
    if n_samples is None:
        # pick a single sample from the dataset
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
        sample_X = X_test.sample(5, random_state=random_state) if n_samples is None else X_test.sample(n_samples, random_state=random_state)
    else:
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
        sample_X = X_test.sample(n_samples, random_state=random_state)

    X_scaled = scaler.transform(sample_X)
    preds = model.predict(X_scaled)
    out = sample_X.copy()
    out["predicted"] = preds
    out.index = range(len(out))
    print(out.head(n_samples or 5))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["train", "predict"], default="train")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--model-path", type=str, default="models/linear_regression.joblib")
    parser.add_argument("--n-samples", type=int, default=5, help="Number of samples to predict when in predict mode")
    parser.add_argument("--plot", action="store_true", help="Plot results (when training)")
    args = parser.parse_args()

    if args.mode == "train":
        X, y = load_data()
        model, scaler, X_test, y_test, preds = train_model(X, y, test_size=args.test_size, random_state=args.random_state, model_path=args.model_path)
        if args.plot:
            plot_results(y_test, preds, save_path=Path(args.model_path).parent / "results.png")
    else:
        out = predict(n_samples=args.n_samples, model_path=args.model_path, random_state=args.random_state)
        if args.plot:
            # optionally plot predicted vs actual using the loaded dataset
            plot_results(out["predicted"].values, out["predicted"].values)


if __name__ == "__main__":
    main()