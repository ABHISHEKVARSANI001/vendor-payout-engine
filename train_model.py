"""
This script implements the model training pipeline for the Vendor Payout & Deduction Engine.
It generates a synthetic future revenue target variable, splits the data, trains a 
Random Forest Regressor, and serializes the model to disk for online inference.
"""

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


def train_payout_forecaster(
    data_path: str = "processed_transactions.csv",
    model_output_path: str = "revenue_predictor.joblib"
) -> None:
    """
    Loads historical processed transaction data, engineers a synthetic revenue projection target,
    trains a RandomForestRegressor model, and serializes the model to the disk.
    
    Args:
        data_path (str): Filepath to the processed CSV containing calculated vendor totals.
        model_output_path (str): Destination filepath to serialize the trained model.
    """
    try:
        # Load the processed transactions dataset
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Historical transaction file '{data_path}' was not found.")
        print("Please ensure your batch processing pipeline or data generator has run first.")
        return

    # Seed the NumPy generator for reproducible synthetic target values
    np.random.seed(42)

    # 1. Engineer a synthetic target variable: 'next_month_revenue'
    # Generates random drift values between -10% (-0.10) and +20% (+0.20)
    growth_decay_factor = np.random.uniform(-0.10, 0.20, size=len(df))
    df["next_month_revenue"] = df["gross_revenue"] * (1 + growth_decay_factor)

    # 2. Separate into features (X) and labels (y)
    feature_cols = ["gross_revenue", "platform_fee_percentage", "variable_tax_percentage"]
    X = df[feature_cols]
    y = df["next_month_revenue"]

    # 3. Split dataset into 80% training and 20% test partitions
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    # 4. Initialize and fit the Random Forest Regressor
    print("Initializing RandomForestRegressor and starting training phase...")
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1  # Use all available CPU cores for execution
    )
    model.fit(X_train, y_train)

    # 5. Model evaluation on the test set
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Model training complete.")
    print(f"Test Set Mean Absolute Error (MAE): {mae:.4f}")

    # 6. Serialize model to disk
    joblib.dump(model, model_output_path)
    print(f"Successfully saved trained model object to '{model_output_path}'.")


if __name__ == "__main__":
    train_payout_forecaster()