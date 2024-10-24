from flask import Flask, request, jsonify
import logging
import requests

app = Flask(__name__)
SECRET_KEY = 'csamt3pr01qobflkbj30'

# Configure logging
logging.basicConfig(level=logging.INFO)

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

    print(f"Processed Symbols with Prices: {prices}")

    return jsonify({'message': 'Symbols processed successfully!', 'symbols': symbols, 'prices': prices}), 200

@app.route('/Kraang', methods=['POST'])
def kraang():
    data = request.get_json()
    logging.info(f"Received request data: {data}")
    
    symbols = data.get('symbols', [])
    prices = {}
    
    for symbol in symbols:
        price = get_stock_price(symbol)
        if price is not None:
            prices[symbol] = {'c': price}
        else:
            logging.warning(f"No price found for {symbol}")

    logging.info(f"Sending response: {prices}")
    return jsonify(prices), 200
    
def get_stock_price(symbol):
    # Finnhub API endpoint for stock price
    finnhub_api_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token=YOUR_FINNHUB_API_KEY"
    try:
        response = requests.get(finnhub_api_url)
        data = response.json()
        return data.get('c')  # Current price
    except Exception as e:
        logging.error(f"Error fetching price for {symbol}: {e}")
        return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
