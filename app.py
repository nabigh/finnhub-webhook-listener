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
    
    # Ensure the request content type is application/json
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415
    
    # Verify the X-Finnhub-Secret header
    if request.headers.get('X-Finnhub-Secret') != os.getenv('FINNHUB_WEBHOOK_SECRET'):
        return jsonify({"error": "Unauthorized request"}), 403

    # Process the JSON body
    try:
        data = request.get_json()
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
