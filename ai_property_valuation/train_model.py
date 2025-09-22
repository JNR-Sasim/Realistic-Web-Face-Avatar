import os
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
MODEL_DIR = PROJECT_DIR / "models"
MODEL_PATH = MODEL_DIR / "property_valuation_model.joblib"
PREPROCESSOR_PATH = MODEL_DIR / "preprocessor.joblib"


def load_or_generate_data() -> pd.DataFrame:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = DATA_DIR / "properties.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)

    # Synthetic data generation as fallback
    rng = np.random.default_rng(42)
    num_rows = 4000

    cities = ["San Francisco", "New York", "Austin", "Seattle", "Denver", "Miami"]
    prop_types = ["house", "apartment", "condo", "townhouse"]

    df = pd.DataFrame({
        "bedrooms": rng.integers(1, 6, size=num_rows),
        "bathrooms": rng.integers(1, 4, size=num_rows) + rng.random(num_rows) * 0.5,
        "sqft": rng.integers(450, 4500, size=num_rows),
        "lot_size": rng.integers(500, 15000, size=num_rows),
        "year_built": rng.integers(1950, 2024, size=num_rows),
        "city": rng.choice(cities, size=num_rows),
        "property_type": rng.choice(prop_types, size=num_rows),
        "has_garage": rng.integers(0, 2, size=num_rows),
        "has_garden": rng.integers(0, 2, size=num_rows),
        "condition_rating": rng.integers(1, 10, size=num_rows),
        "walk_score": rng.integers(10, 100, size=num_rows),
        "school_score": rng.integers(10, 100, size=num_rows),
        "crime_index": rng.integers(10, 100, size=num_rows),
    })

    # Price generation with semi-realistic relationships
    base_city_factor = df["city"].map({
        "San Francisco": 1000,
        "New York": 950,
        "Seattle": 700,
        "Austin": 550,
        "Denver": 520,
        "Miami": 600,
    }).fillna(500)

    type_factor = df["property_type"].map({
        "house": 1.0,
        "townhouse": 0.9,
        "condo": 0.85,
        "apartment": 0.8,
    }).fillna(0.85)

    age = 2025 - df["year_built"]

    price = (
        50 * df["sqft"]
        + 50000 * df["bedrooms"]
        + 40000 * df["bathrooms"]
        + 2 * df["lot_size"]
        + 10000 * df["has_garage"]
        + 8000 * df["has_garden"]
        + 7000 * df["condition_rating"]
        + 3000 * (df["walk_score"] / 10)
        + 4000 * (df["school_score"] / 10)
        - 2500 * (df["crime_index"] / 10)
    ) * type_factor + base_city_factor * 100

    # Penalize older homes slightly, add noise
    price = price - 500 * age + rng.normal(0, 60000, size=num_rows)

    df["price"] = np.maximum(price, 50000).round(0)

    return df


def build_preprocessor(numeric_features: list, categorical_features: list) -> ColumnTransformer:
    numeric_transformer = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )
    return preprocessor


def train_and_save_model(df: pd.DataFrame) -> Tuple[Pipeline, float]:
    feature_cols = [
        "bedrooms", "bathrooms", "sqft", "lot_size", "year_built",
        "city", "property_type", "has_garage", "has_garden",
        "condition_rating", "walk_score", "school_score", "crime_index",
    ]
    target_col = "price"

    X = df[feature_cols]
    y = df[target_col]

    numeric_features = [
        "bedrooms", "bathrooms", "sqft", "lot_size", "year_built",
        "condition_rating", "walk_score", "school_score", "crime_index",
    ]
    categorical_features = ["city", "property_type", "has_garage", "has_garden"]

    preprocessor = build_preprocessor(numeric_features, categorical_features)

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    mae = float(mean_absolute_error(y_test, preds))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    # Also save preprocessor separately (handy for feature metadata)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)

    return pipeline, mae


def main():
    df = load_or_generate_data()
    _, mae = train_and_save_model(df)
    print(f"Model trained and saved to {MODEL_PATH}. Test MAE: ${mae:,.0f}")


if __name__ == "__main__":
    main()

