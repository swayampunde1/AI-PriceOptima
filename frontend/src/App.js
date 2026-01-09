import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    Unit_Price: 25.50,
    price_lag_1d: 25.50,
    price_lag_7d: 25.00,
    sales_lag_1d: 3.0,
    sales_lag_7d: 4.0,
    sales_rolling_avg_7d: 3.5,
    day_of_week: 5,
    is_weekend: 1,
    month: 10
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    setTimeout(async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/predict', formData);
            setResult(response.data);
        } catch (err) {
            console.error(err);
            setError('❌ Backend disconnected. Please restart the Python terminal.');
        }
        setLoading(false);
    }, 800);
  };

  return (
    <div className="App">
      <div className="dashboard-container">
        <header>
          <h1>📦 PriceOptima Pro</h1>
          <p>Advanced Dynamic Pricing Control</p>
        </header>

        <form onSubmit={handleSubmit} className="form-grid">
            {/* Row 1 */}
            <label>
                <span>💰 Product Price ($)</span>
                <input name="Unit_Price" type="number" step="0.01" value={formData.Unit_Price} onChange={handleChange} />
            </label>

            <label>
                <span>📉 Yesterday's Sales (Qty)</span>
                <input name="sales_lag_1d" type="number" value={formData.sales_lag_1d} onChange={handleChange} />
            </label>

            {/* Row 2 */}
            <label>
                <span>📊 Avg Sales (7 Days)</span>
                <input name="sales_rolling_avg_7d" type="number" step="0.1" value={formData.sales_rolling_avg_7d} onChange={handleChange} />
            </label>

            <label>
                <span>📅 Month (1-12)</span>
                <input name="month" type="number" min="1" max="12" value={formData.month} onChange={handleChange} />
            </label>

            {/* Row 3 */}
            <label>
                <span>📆 Day of Week (0=Mon, 6=Sun)</span>
                <input name="day_of_week" type="number" min="0" max="6" value={formData.day_of_week} onChange={handleChange} />
            </label>

            <label>
                <span>🚦 Is Weekend? (1=Yes, 0=No)</span>
                <input name="is_weekend" type="number" min="0" max="1" value={formData.is_weekend} onChange={handleChange} />
            </label>

            <button type="submit" disabled={loading} className="optimize-btn">
                {loading ? '🔄 Analyzing Market Data...' : '🚀 Calculate Optimal Price'}
            </button>
        </form>
        
        {error && <p className="error-msg">{error}</p>}

        {result && (
            <div className="result-section">
                <div className="result-row">
                    <span>Market Condition:</span>
                    <span className="val">{result.predicted_revenue > 45 ? 'High Demand 🔥' : 'Stable'}</span>
                </div>
                <div className="result-row">
                    <span>Current Strategy:</span>
                    <span className="val">${result.current_price}</span>
                </div>
                <div className="result-row">
                    <span style={{color: '#4ade80', fontWeight: 'bold'}}>AI Suggested Price:</span>
                    <span className="val-large">${result.recommended_price}</span>
                </div>
                
                {result.uplift_detected ? (
                    <div className="badge success">📈 Opportunity Detected!</div>
                ) : (
                    <div className="badge neutral">✅ Price is Optimized</div>
                )}
            </div>
        )}

      </div>
    </div>
  );
}

export default App;
