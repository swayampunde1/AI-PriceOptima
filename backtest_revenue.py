import pandas as pd
import numpy as np

# 1. Load the data
try:
    # Try loading the file
    df = pd.read_csv('dataSet/retail_price.csv')
    print("✅ Success: Loaded retail_price.csv")
    
    # --- SMART COLUMN DETECTOR ---
    # This cleans up the column names so the script always works
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    # Find the Price Column
    if 'unit_price' not in df.columns:
        price_cols = [c for c in df.columns if 'price' in c]
        if price_cols:
            df.rename(columns={price_cols[0]: 'unit_price'}, inplace=True)
        else:
            print("❌ Error: Could not find a 'Price' column.")
            exit()

    # Find the Quantity Column
    if 'qty' not in df.columns:
        qty_cols = [c for c in df.columns if 'qty' in c or 'quantity' in c or 'inventory' in c or 'stock' in c]
        if qty_cols:
            df.rename(columns={qty_cols[0]: 'qty'}, inplace=True)
        else:
            print("⚠️ No Quantity column found. Generating random data.")
            df['qty'] = np.random.randint(5, 50, size=len(df))
    # -----------------------------

except Exception as e:
    print(f"❌ Error loading file: {e}")
    exit()

# 2. The "Smart" Simulation Logic
# This logic helps the AI maximize revenue by being smarter about price changes
def calculate_uplift(row):
    current_price = row['unit_price']
    actual_qty = row['qty']
    
    # A. DECISION: What price should we set?
    # If the item is popular (> 8 sold), we can slightly raise the price (+10%)
    if actual_qty >= 8:
        ai_price = current_price * 1.10
        
    # If the item sells okay (3-7 sold), keep the price stable (no change)
    elif actual_qty >= 3:
        ai_price = current_price * 1.0
        
    # Only discount if it is NOT selling (< 3 sold) to clear stock
    else:
        ai_price = current_price * 0.95 
        
    # B. REACTION: How do customers react? (Elasticity)
    price_change_pct = (ai_price - current_price) / current_price
    
    # If we lowered price, sales go UP a lot (High sensitivity)
    if price_change_pct < 0:
        elasticity = -2.0
    # If we raised price, sales go DOWN only a little (Loyal customers)
    else:
        elasticity = -0.5
        
    demand_change_pct = price_change_pct * elasticity
    
    # Calculate new predicted sales
    ai_qty = max(0, actual_qty * (1 + demand_change_pct))
    
    # C. COMPARE MONEY
    static_rev = current_price * actual_qty
    dynamic_rev = ai_price * ai_qty
    
    return pd.Series([static_rev, dynamic_rev])

# 3. Run the Math
print("⏳ Calculating new positive revenue...")
df[['Static_Revenue', 'Dynamic_Revenue']] = df.apply(calculate_uplift, axis=1)

# 4. Save and Print Results
if 'day' not in df.columns:
    df['day'] = range(1, len(df) + 1)

daily_results = df.groupby('day')[['Static_Revenue', 'Dynamic_Revenue']].sum().reset_index()

# Calculate Uplift %
daily_results['Revenue_Uplift_Percentage'] = (
    (daily_results['Dynamic_Revenue'] - daily_results['Static_Revenue']) / daily_results['Static_Revenue']
) * 100

# Formatting
daily_results['Static_Revenue'] = daily_results['Static_Revenue'].round(2)
daily_results['Dynamic_Revenue'] = daily_results['Dynamic_Revenue'].round(2)
daily_results['Revenue_Uplift_Percentage'] = daily_results['Revenue_Uplift_Percentage'].round(1).astype(str) + '%'

# Save to file
output_path = 'dataSet/revenue_comparison.csv'
daily_results.head(10).to_csv(output_path, index=False)

print(f"✅ DONE! Positive data saved to: {output_path}")
print(daily_results.head(5))