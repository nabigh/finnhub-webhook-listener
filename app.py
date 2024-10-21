import os
from flask import Flask, request, jsonify
import finnhub

app = Flask(__name__)

# Set the API key for Finnhub from environment variable
finnhub_client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY'))

# Route for Finnhub webhook events
@app.route('/finnhub-webhook', methods=['POST'])
def finnhub_webhook():
    # Verify the X-Finnhub-Secret header
    if request.headers.get('X-Finnhub-Secret') != os.getenv('FINNHUB_WEBHOOK_SECRET'):
        return jsonify({"error": "Unauthorized request"}), 403
    
    # Log the incoming request for debugging
    print(f"Headers: {request.headers}")
    print(f"Body: {request.get_data(as_text=True)}")

    # Handle the webhook event data
    data = request.json
    event = data.get('event')

    if event == 'earnings':
        print("Earnings event received:")
        print(data)
    
    # Respond with a success message
    return jsonify({"status": "success"}), 200

# Route to fetch stock price
@app.route('/stock-price/<symbol>', methods=['GET'])
def stock_price(symbol):
    try:
        quote = finnhub_client.quote(symbol)
        return jsonify(quote)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main entry point
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
