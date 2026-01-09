
# PriceOptima: AI-Based Dynamic Pricing Optimization System

### 1. Project Objective

The primary objective of **PriceOptima** is to address the limitations of traditional static pricing in the retail sector. By leveraging Machine Learning, this project aims to:

* Develop an AI system that automatically adjusts prices based on real-time market conditions (demand, seasonality, and stock levels).


* Maximize **Total Revenue** and **Profit Margins** while maintaining competitive positioning.


* Optimize inventory turnover to reduce holding costs and stockouts.



### 2. Dataset Description

The project utilizes a comprehensive retail transaction dataset containing historical records of pricing, sales performance, and inventory status.

* 
**Source:** Aggregated retail transaction logs and inventory records.


* **Key Features:**
* **Price:** Historical unit price (including discounts).
* **Demand (Sales Qty):** Daily units sold (Target Variable).
* **Inventory:** Daily stock levels.
* 
**Temporal Data:** Date, Month, Day of Week, Weekend indicators.




* 
**Data Processing:** Performed extensive cleaning, outlier detection, and imputation for missing inventory/price values.



### 3. Technologies Used

* **Machine Learning:** Python, Scikit-Learn, XGBoost, Pandas, NumPy.
* 
**Backend API:** FastAPI, Uvicorn (for real-time inference).


* 
**Frontend Dashboard:** React.js, Axios, CSS3 (for visualization and user interaction).


* 
**Tools:** VS Code, Swagger UI (for API testing), Git.



### 4. Model Development Summary

The core "Brain" of the system was developed through a rigorous ML pipeline:

1. 
**EDA (Exploratory Data Analysis):** Confirmed the inverse correlation between price and demand and identified seasonal demand spikes.


2. 
**Feature Engineering:** Created Lag features (e.g., `sales_lag_1d`, `price_lag_7d`) and Rolling Averages to capture trends.


3. 
**Model Training:** Trained **XGBoost Regressor** and **LightGBM** models to predict demand elasticity.


4. 
**Optimization Logic:** The algorithm simulates demand at various price points (-20% to +30%) to identify the specific price that maximizes **Predicted Revenue**.



### 5. Backend Implementation (FastAPI)

A high-performance REST API serves as the bridge between the AI model and the user interface.

* **Framework:** FastAPI.
* **Functionality:**
* Loads the trained XGBoost model (`.pkl`) on startup.


* Defines input data schemas using Pydantic (ensuring data validity).
* Exposes a `/predict` endpoint that accepts product parameters and returns the **Recommended Price**, **Predicted Revenue**, and **Uplift Status**.


* Implements CORS middleware to allow secure communication with the frontend.



### 6. Dashboard Implementation (React.js)

The frontend provides an intuitive "Control Tower" for Store Managers.

* **Framework:** React.js.
* **Features:**
* 
**Interactive Form:** Allows input of real-time variables (Current Price, Recent Sales, Stock, Date).


* **Visual Feedback:** Displays color-coded results (Green for Revenue Uplift) to indicate positive pricing opportunities.
* 
**Real-Time Connection:** Uses `Axios` to send asynchronous requests to the FastAPI backend.




* **Design:** Modern, dark-themed UI for professional usability.

### 7. Deployment / Execution Approach

The system is designed for local deployment with a simplified execution flow.

**Prerequisites:** Python 3.x, Node.js.

**Steps to Run:**

1. **Backend (Terminal 1):**
```bash
python -m uvicorn main:app --reload

```


*Starts the AI server at [http://127.0.0.1:8000*](http://127.0.0.1:8000)
2. **Frontend (Terminal 2):**
```bash
cd price_optima_dashboard
npm start

```


*Launches the dashboard at http://localhost:3000*

*(Optional: A `Start_PriceOptima.bat` script is included for one-click launch).*

### 8. Key Outputs & Results

* 
**Revenue Uplift:** The AI-driven pricing strategy demonstrated a quantifiable increase in total revenue compared to static pricing during backtesting.


* 
**Smart Sensitivity:** The model successfully detects high-demand scenarios (e.g., weekends/holidays) and suggests premium pricing, while recommending discounts during low-sales periods to recover volume.


* **Operational Efficiency:** Automated pricing decisions reduce the manual workload for store managers.

### 9. Conclusion and Future Enhancements

**Conclusion:**
PriceOptima successfully bridges the gap between raw data and actionable business strategy. By moving from static rules to AI-driven elasticity modeling, the system provides a robust solution for maximizing retail profitability.

**Future Enhancements:**

* **Competitor Pricing:** Integrate API feeds from competitor websites to adjust prices relative to the market.
* **Multi-Product Support:** Scale the dashboard to handle bulk pricing uploads via CSV.
* **Cloud Deployment:** Deploy the solution to AWS/Azure for remote accessibility.