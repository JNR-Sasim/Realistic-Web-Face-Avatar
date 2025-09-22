from pathlib import Path
from typing import Literal, Optional

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "models" / "property_valuation_model.joblib"


class PropertyFeatures(BaseModel):
    bedrooms: int = Field(ge=0, le=20)
    bathrooms: float = Field(ge=0, le=20)
    sqft: int = Field(ge=100, le=20000)
    lot_size: int = Field(ge=0, le=200000)
    year_built: int = Field(ge=1800, le=2100)
    city: str
    property_type: Literal["house", "apartment", "condo", "townhouse"]
    has_garage: int = Field(ge=0, le=1)
    has_garden: int = Field(ge=0, le=1)
    condition_rating: int = Field(ge=1, le=10)
    walk_score: int = Field(ge=0, le=100)
    school_score: int = Field(ge=0, le=100)
    crime_index: int = Field(ge=0, le=100)


class PredictionResponse(BaseModel):
    predicted_price: float
    currency: str = "USD"
    model_version: Optional[str] = None


app = FastAPI(title="AI Property Valuation API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def load_model():
    if not MODEL_PATH.exists():
        # Lazy train if model missing
        from .train_model import main as train_main
        train_main()

    app.state.model = joblib.load(MODEL_PATH)


@app.get("/")
def root():
    return {"message": "AI Property Valuation API is running", "docs": "/docs"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: PropertyFeatures):
    model = app.state.model
    # Build a DataFrame so ColumnTransformer can index by column names
    data = {
        "bedrooms": [features.bedrooms],
        "bathrooms": [features.bathrooms],
        "sqft": [features.sqft],
        "lot_size": [features.lot_size],
        "year_built": [features.year_built],
        "city": [features.city],
        "property_type": [features.property_type],
        "has_garage": [features.has_garage],
        "has_garden": [features.has_garden],
        "condition_rating": [features.condition_rating],
        "walk_score": [features.walk_score],
        "school_score": [features.school_score],
        "crime_index": [features.crime_index],
    }
    X_df = pd.DataFrame(data)

    pred = float(model.predict(X_df)[0])
    return PredictionResponse(predicted_price=max(pred, 0.0))

