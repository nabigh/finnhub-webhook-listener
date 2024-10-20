from flask import Flask, request, jsonify

app = Flask(__name__)

# Finnhub Webhook Route - Allow both POST and GET methods
@app.route('/finnhub-webhook', methods=['POST', 'GET'])
def finnhub_webhook():
    # Acknowledge GET requests to indicate that the endpoint is active
    if request.method == 'GET':
        return jsonify({"message": "Webhook is active and ready to receive POST requests."}), 200

    # For POST requests, we acknowledge receipt before any processing
    if request.method == 'POST':
        headers = request.headers

        # Verify the secret key for authentication
        if headers.get('X-Finnhub-Secret') != 'csamt3pr01qobflkbj30':
            return jsonify({"error": "Invalid secret key"}), 403

        # Acknowledge receipt of the event immediately
        # This is crucial to prevent timeouts
        # Return a 200 status code to confirm receipt
        acknowledgement_response = jsonify({"status": "received"}), 200
        
        # Process the incoming data after acknowledging the receipt
        data = request.json
        print("Received Webhook Event:", data)

        # (Optional) Here you could implement your trading logic
        # For example, trigger trades based on the received event

        return acknowledgement_response  # Return the acknowledgement response

if __name__ == '__main__':
    app.run(port=5000, debug=True)
