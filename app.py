from flask import Flask, request, jsonify
import os
import logging
import requests

app = Flask(__name__)

# Enable logging for better debugging
logging.basicConfig(level=logging.DEBUG)

# Environment variable for secret key
FINNHUB_WEBHOOK_SECRET = os.getenv('FINNHUB_WEBHOOK_SECRET', 'csamt3pr01qobflkbj30')

@app.route('/finnhub-webhook', methods=['POST'])
def finnhub_webhook():
    # Log request headers, content type, and body for debugging
    logging.info("Request Headers: %s", request.headers)
    logging.info("Request Content-Type: %s", request.content_type)
    logging.info("Request Body: %s", request.get_data(as_text=True))
    
    # Check for missing Content-Type and assume JSON if missing
    if request.content_type is None or request.content_type != 'application/json':
        logging.warning("Missing or incorrect Content-Type. Assuming application/json.")
        try:
            data = request.get_json(force=True)  # Force Flask to treat body as JSON
        except Exception as e:
            logging.error(f"Error parsing JSON body: {str(e)}")
            return jsonify({"error": "Invalid JSON body"}), 400
    else:
        data = request.get_json()

    # Verify the X-Finnhub-Secret header
    if request.headers.get('X-Finnhub-Secret') != FINNHUB_WEBHOOK_SECRET:
        return jsonify({"error": "Unauthorized request"}), 403

    # Process the JSON body
    try:
        if not data:
            raise ValueError("No JSON body found")
        logging.info("Received JSON: %s", data)

        # Handle the webhook data
        if data.get('event') == 'earnings':
            logging.info(f"Earnings data: {data['data']}")

        # Fetch stock data (Example)
        stock_symbols = data.get('symbols', [])
        stock_data = fetch_stock_data(stock_symbols)

        if not stock_data:
            logging.warning("No stock data retrieved.")
            return jsonify({"error": "No stock data found"}), 404
        
        logging.info("Retrieved stock data: %s", stock_data)
        return jsonify({"status": "success", "data": stock_data}), 200

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

def fetch_stock_data(symbols):
    stock_data = {}
    for symbol in symbols:
        try:
            # Example Finnhub API call to get current price
            response = requests.get(f'https://finnhub.io/api/v1/quote?symbol={symbol}&token=csamt3pr01qobflkbj1gcsamt3pr01qobflkbj20')
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            # Ensure the necessary data is available
            if 'c' in data:
                stock_data[symbol] = {'current_price': data['c']}
            else:
                logging.warning(f"No current price found for {symbol}.")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred for {symbol}: {http_err}")
        except Exception as e:
            logging.error(f"Failed to retrieve data for {symbol}: {e}")
    
    return stock_data

# Flask app settings
if __name__ == "__main__":
    app.run(debug=True)
