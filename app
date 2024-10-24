from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)

# Enable logging for better debugging
logging.basicConfig(level=logging.DEBUG)

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

# Flask app settings
if __name__ == "__main__":
    app.run(debug=True)
