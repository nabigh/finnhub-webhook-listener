from flask import Flask, request, jsonify
import logging
import requests

app = Flask(__name__)
SECRET_KEY = 'csamt3pr01qobflkbj30'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Webhook to receive stock symbols and process them (restoring the original functionality)
@app.route('/finnhub-webhook', methods=['POST'])
def receive_symbols():
    data = request.get_json()
    logging.info(f"Received data: {data}")

    # Validate the secret key
    if data.get('secret') != SECRET_KEY:
        return jsonify({'error': 'Invalid secret key'}), 403

    # Extract stock symbols
    symbols = data.get('symbols', [])
    logging.info(f"Processing symbols: {symbols}")

    # Process the symbols by fetching their latest prices from Finnhub
    prices = {}
    for symbol in symbols:
        price = get_stock_price(symbol)
        prices[symbol] = price

    logging.info(f"Processed Symbols with Prices: {prices}")

    return jsonify({'message': 'Symbols processed successfully!', 'symbols': symbols, 'prices': prices}), 200

# Route specifically for Kraang (new functionality for Kraang to retrieve data)
@app.route('/Kraang', methods=['POST'])
def kraang_data():
    data = request.get_json()
    logging.info(f"Kraang requested data for symbols: {data}")

    # Validate the secret key
    if data.get('secret') != SECRET_KEY:
        return jsonify({'error': 'Unauthorized request'}), 403

    # Extract stock symbols
    symbols = data.get('symbols', [])
    logging.info(f"Fetching data for Kraang symbols: {symbols}")

    # Process the symbols by fetching their latest prices from Finnhub
    stock_data = {}
    for symbol in symbols:
        price = get_stock_price(symbol)
        stock_data[symbol] = price

    logging.info(f"Sending stock data to Kraang: {stock_data}")
    return jsonify({'stock_data': stock_data}), 200

def get_stock_price(symbol):
    # Finnhub API endpoint for stock price (replace YOUR_FINNHUB_API_KEY with actual API key)
    finnhub_api_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token=YOUR_FINNHUB_API_KEY"
    try:
        response = requests.get(finnhub_api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('c')  # Return the current price (if available)
        else:
            logging.error(f"Failed to fetch price for {symbol}. Status code: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error fetching price for {symbol}: {e}")
        return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
