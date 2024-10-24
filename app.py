from flask import Flask, request, jsonify
import logging
import requests

app = Flask(__name__)
SECRET_KEY = 'csamt3pr01qobflkbj30'

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/Kraang', methods=['POST'])
def kraang():
    data = request.get_json()
    logging.info(f"Received request data: {data}")
    
    if not data or 'symbols' not in data:
        logging.warning("No symbols provided in the request.")
        return jsonify({}), 400  # Return empty response with 400 Bad Request
    
    symbols = data['symbols']
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
        logging.info(f"Data fetched for {symbol}: {data}")
        return data.get('c')  # Current price
    except Exception as e:
        logging.error(f"Error fetching price for {symbol}: {e}")
        return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
