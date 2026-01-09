# AI-PriceOptima: Dynamic Pricing Optimization System

## 1. Project Objective
The objective of this project is to develop an AI-powered dynamic pricing system that optimizes retail product prices to maximize total revenue. By analyzing historical sales data, the system predicts the optimal price point for products, balancing demand and profit margins.

## 2. Dataset Description
The system uses a retail sales dataset (`dataSet/retail_price.csv`) which includes:
* **Product ID & Category:** Information about specific items.
* **Unit Price & Cost:** Historical pricing strategies.
* **Sales Volume:** Quantity sold at different price points.
* **Competitor Prices:** External market data for benchmarking.

## 3. Technologies Used
* **Frontend:** React.js, HTML5, CSS3 (Interactive Dashboard)
* **Backend:** Python (FastAPI/Flask)
* **Machine Learning:** Scikit-Learn (Model Training), Pandas (Data Processing), NumPy
* **Tools:** VS Code, Git, GitHub

## 4. Model Development Summary
We utilized a **Random Forest Regressor** (or Linear Regression) to model the relationship between price and sales volume.
* **Feature Engineering:** Created features such as price elasticity and seasonality.
* **Training:** The model was trained on historical data to predict future demand at various price points.
* **Serialization:** The trained model is saved as `price_optimization_model.pkl` for real-time inference.

## 5. Backend Implementation
The backend (`main.py`) serves as the bridge between the machine learning model and the frontend dashboard.
* It loads the `price_optimization_model.pkl` file.
* It exposes API endpoints that accept product data and return the recommended optimal price.
* It handles data validation and formatting before passing it to the model.

## 6. Dashboard Implementation (React.js)
The frontend (`frontend/` folder) provides a user-friendly interface for store managers.
* **Features:** Displays current prices vs. recommended optimized prices.
* **Visualization:** Charts showing potential revenue uplift.
* **Interactivity:** Users can filter by product category and view specific predictions.

## 7. Deployment / Execution Approach
To run this project locally:

**Step 1: Clone the Repository**
```bash
git clone [https://github.com/swayampunde1/AI-PriceOptima.git](https://github.com/swayampunde1/AI-PriceOptima.git)
cd AI-PriceOptima
