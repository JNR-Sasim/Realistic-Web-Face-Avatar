## AI Property Valuation Tool

An end-to-end property price prediction app:
- Model training (with synthetic data fallback)
- FastAPI prediction service
- Simple web UI for inputs

### Features
- Numeric and categorical features with proper preprocessing
- RandomForest model with prediction uncertainty estimate
- CORS-enabled API and Swagger docs at /docs

### Tech Stack
- Python, scikit-learn, pandas, numpy, joblib
- FastAPI, Uvicorn
- Vanilla HTML/JS frontend

### Quick Start
1) Create a virtual environment and install deps:
```
python -m venv .venv
.venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

2) Train the model (uses synthetic data if no CSV provided):
```
python ai_property_valuation/train_model.py
```

3) Start the API server:
```
uvicorn ai_property_valuation.api:app --reload
```

4) Open the UI:
- Open `ai_property_valuation/ui/property_valuation.html` in your browser
- Or use the interactive docs at `http://127.0.0.1:8000/docs`

### Using Your Own Data (Optional)
- Place a CSV at `ai_property_valuation/data/properties.csv` with columns:
  - bedrooms, bathrooms, sqft, lot_size, year_built,
  - city, property_type, has_garage, has_garden,
  - condition_rating, walk_score, school_score, crime_index,
  - price
- Then rerun the training command above.

