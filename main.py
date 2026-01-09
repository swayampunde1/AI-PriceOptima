from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (Allows React to talk to Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the AI Model
try:
    model = joblib.load("price_optimization_model.pkl")
    print("✅ Success: XGBoost Model loaded.")
except:
    print("⚠️ Warning: Model not found. Using simulation mode for testing.")
    model = None

# --- UPGRADED INPUT STRUCTURE ---
# Now accepting all the new fields you added to the dashboard
class ProductInput(BaseModel):
    Unit_Price: float
    price_lag_1d: float = 25.50
    price_lag_7d: float = 25.00
    sales_lag_1d: float
    sales_lag_7d: float = 4.0
    sales_rolling_avg_7d: float
    day_of_week: int
    is_weekend: int
    month: int

@app.post("/predict")
def predict_price(data: ProductInput):
    current_price = data.Unit_Price
    
    # 1. EXPANDED SEARCH RANGE
    # The AI will now test prices from -20% to +30% of the current price
    price_multipliers = [0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2, 1.3]
    candidate_prices = [round(current_price * m, 2) for m in price_multipliers]

    best_price = current_price
    best_revenue = -1
    base_revenue = 0

    # 2. SIMULATION LOOP
    for test_price in candidate_prices:
        # Prepare data for the AI
        input_data = pd.DataFrame([{
            "Unit_Price": test_price,
            "price_lag_1d": data.price_lag_1d,
            "price_lag_7d": data.price_lag_7d,
            "sales_lag_1d": data.sales_lag_1d,
            "sales_lag_7d": data.sales_lag_7d,
            "sales_rolling_avg_7d": data.sales_rolling_avg_7d,
            "day_of_week": data.day_of_week,
            "is_weekend": data.is_weekend,
            "month": data.month
        }])

        # Predict Sales (Qty)
        if model:
            try:
                # Ensure columns match training data order exactly
                required_cols = ["Unit_Price", "price_lag_1d", "price_lag_7d", "sales_lag_1d", 
                               "sales_lag_7d", "sales_rolling_avg_7d", "day_of_week", "is_weekend", "month"]
                
                # Fill missing cols if model expects more, just to be safe
                for col in required_cols:
                    if col not in input_data.columns:
                        input_data[col] = 0
                
                predicted_qty = model.predict(input_data[required_cols])[0]
            except:
                # Fallback logic if model columns mismatch
                predicted_qty = max(0, 50 - (test_price * 1.5) + (data.sales_lag_1d * 0.5)) 
        else:
            # Simulation Logic (if no model file)
            # Higher price = Lower sales, Higher past sales = Higher future sales
            base_demand = 10 
            price_sensitivity = 1.2
            sales_boost = (data.sales_lag_1d * 0.8) + (data.sales_rolling_avg_7d * 0.5)
            
            # If weekend, boost demand
            if data.is_weekend == 1:
                sales_boost *= 1.2
            
            predicted_qty = max(0, base_demand - (test_price * 0.1 * price_sensitivity) + sales_boost)

        # Calculate Revenue
        revenue = predicted_qty * test_price

        # Save the result for the current price (Base Case)
        if test_price == current_price:
            base_revenue = revenue

        # Check if this is the new best price
        if revenue > best_revenue:
            best_revenue = revenue
            best_price = test_price

    return {
        "status": "success",
        "current_price": current_price,
        "recommended_price": float(best_price),
        "predicted_revenue": round(float(best_revenue), 2),
        "uplift_detected": best_price != current_price
    }

@app.get("/")
def home():
    return {"message": "PriceOptima API is Running!"}