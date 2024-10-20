# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Secret key for webhook validation
FINNHUB_SECRET = "csamt3pr01qobflkbj30"  # Replace with your Finnhub secret

@app.route('/finnhub-webhook', methods=['POST'])
def finnhub_webhook():
    headers = request.headers
    
    # Validate the incoming request
    if headers.get('X-Finnhub-Secret') != FINNHUB_SECRET:
        return jsonify({"error": "Invalid secret key"}), 403
    
    # Process the received event data
    data = request.json
    print("Received Webhook Event:", data)
    
    # Implement your trading logic here based on the event data

    # Acknowledge receipt of the event
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
