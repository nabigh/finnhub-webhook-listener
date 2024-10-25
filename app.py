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
    # UNTOUCHABLE: Log request headers, content type, and body for debugging
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

        return jsonify({"status": "success"}), 200

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

@app.route('/Kraang', methods=['POST'])
def kraang_endpoint():
    # Endpoint for Kraang to fetch stock data
    logging.info("Kraang endpoint called.")
    data = request.get_json()

    if not data or 'symbols' not in data:
        return jsonify({"error": "No symbols provided"}), 400

    symbols = data['symbols']
    stock_data = fetch_stock_data(symbols)
    
    if not stock_data:
        return jsonify({"error": "No stock data found"}), 404

    logging.info("Stock data for Kraang: %s", stock_data)
    return jsonify({"status": "success", "data": stock_data}), 200

# Flask app settings
if __name__ == "__main__":
    app.run(debug=True)
