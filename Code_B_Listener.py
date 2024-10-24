import os
import requests
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

app = Flask(__name__)

# Your Finnhub API key (use environment variables in production)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "your_finnhub_api_key_here")
BASE_URL = "https://finnhub.io/api/v1"

# Function to get historical stock data from Finnhub
def get_stock_data(symbol):
    today = datetime.now()
    past = today - timedelta(days=365)  # Fetch last 1 year of data

    # Convert to UNIX timestamp
    to_time = int(today.timestamp())
    from_time = int(past.timestamp())

    url = f"{BASE_URL}/stock/candle"
    params = {
        "symbol": symbol,
        "resolution": "D",  # Daily data
        "from": from_time,
        "to": to_time,
        "token": FINNHUB_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and data['s'] == 'ok':
        return pd.DataFrame({
            "Date": pd.to_datetime(data['t'], unit='s'),
            "Open": data['o'],
            "High": data['h'],
            "Low": data['l'],
            "Close": data['c'],
            "Volume": data['v']
        })
    else:
        print(f"Failed to retrieve data for {symbol}")
        return None

# Basic trading signal logic (can be expanded into more complex models)
def generate_signals(df):
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()

    last_price = df['Close'].iloc[-1]
    last_sma50 = df['SMA_50'].iloc[-1]
    last_sma200 = df['SMA_200'].iloc[-1]

    if last_sma50 > last_sma200 and last_price > last_sma50:
        return 'BUY'
    elif last_sma50 < last_sma200 and last_price < last_sma50:
        return 'SELL'
    else:
        return 'HOLD'

# Machine learning logic (placeholder for actual ML model)
def run_ml_model(df):
    # Simple linear regression to predict next day's close price
    df['Returns'] = df['Close'].pct_change()

    df = df.dropna()  # Drop NaN values

    X = np.array(range(len(df))).reshape(-1, 1)
    y = df['Close'].values

    model = LinearRegression()
    model.fit(X, y)

    next_day_prediction = model.predict([[len(df)]])
    last_close = df['Close'].iloc[-1]

    if next_day_prediction > last_close:
        return 'BUY'
    elif next_day_prediction < last_close:
        return 'SELL'
    else:
        return 'HOLD'

# Webhook endpoint to receive stock symbols and process them
@app.route("/finnhub-webhook", methods=["POST"])
def process_webhook():
    data = request.json
    event = data.get('event')
    symbols_data = data.get('data', [])
    
    if event == "earnings" or event == "stocks_update":  # Adjust event name based on Code A
        results = []
        
        for symbol_data in symbols_data:
            symbol = symbol_data.get('symbol')
            stock_df = get_stock_data(symbol)
            
            if stock_df is not None:
                basic_signal = generate_signals(stock_df)
                ml_signal = run_ml_model(stock_df)

                results.append({
                    "symbol": symbol,
                    "basic_signal": basic_signal,
                    "ml_signal": ml_signal
                })
        
        return jsonify(results)
    
    return jsonify({"message": "Invalid event"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
