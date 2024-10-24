from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)

# Enable logging for better debugging
logging.basicConfig(level=logging.DEBUG)

# Original Route: Finnhub Webhook listener (unchanged)
@app.route('/finnhub-webhook', methods=['POST'])
def finnhub_webhook():
    # Log request headers, content type, and body for debugging
    print("Request Headers:", request.headers)
    print("Request Content-Type:", request.content_type)
    print("Request Body:", request.get_data(as_text=True))
    
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
    if request.headers.get('X-Finnhub-Secret') != os.getenv('FINNHUB_WEBHOOK_SECRET'):
        return jsonify({"error": "Unauthorized request"}), 403

    # Process the JSON body
    try:
        if not data:
            raise ValueError("No JSON body found")
        print("Received JSON:", data)

        # Handle the webhook data (you can add more logic here)
        if data.get('event') == 'earnings':
            print(f"Earnings data: {data['data']}")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        # Log the error for debugging
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

# New Route: Kraang to request stock data (new functionality)
@app.route('/Kraang', methods=['POST'])
def kraang_data():
    # Log the incoming request
    print("Kraang Request Body:", request.get_data(as_text=True))

    # Check for missing Content-Type and assume JSON if missing
    if request.content_type is None or request.content_type != 'application/json':
        logging.warning("Missing or incorrect Content-Type. Assuming application/json.")
        try:
            data = request.get_json(force=True)
        except Exception as e:
            logging.error(f"Error parsing JSON body: {str(e)}")
            return jsonify({"error": "Invalid JSON body"}), 400
    else:
        data = request.get_json()

    # Verify the secret key in the request body
    if data.get('secret') != os.getenv('FINNHUB_WEBHOOK_SECRET'):
        return jsonify({"error": "Unauthorized request"}), 403

    # Process the JSON body to extract stock symbols
    try:
        symbols = data.get('symbols', [])
        if not symbols:
            return jsonify({"error": "No symbols provided"}), 400

        print("Processing symbols for Kraang:", symbols)

        # Simulate fetching stock data for the requested symbols (logic can be expanded)
        stock_data = {}
        for symbol in symbols:
            # Example data, replace with actual Finnhub API call
            stock_data[symbol] = {"current_price": 100.0, "volume": 10000}

        return jsonify({"stock_data": stock_data}), 200

    except Exception as e:
        logging.error(f"Error processing Kraang data request: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

# Flask app settings
if __name__ == "__main__":
    app.run(debug=True)
