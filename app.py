from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/finnhub-webhook', methods=['POST', 'GET'])
def finnhub_webhook():
    # Acknowledge GET requests
    if request.method == 'GET':
        return jsonify({"message": "Webhook is active and ready to receive POST requests."}), 200

    # For POST requests
    if request.method == 'POST':
        # Check the Content-Type header
        if request.content_type != 'application/json':
            return jsonify({"error": "Content-Type must be application/json"}), 415

        headers = request.headers

        # Verify the secret key for authentication
        if headers.get('X-Finnhub-Secret') != 'csamt3pr01qobflkbj30':
            return jsonify({"error": "Invalid secret key"}), 403

        # Acknowledge receipt of the event immediately
        acknowledgement_response = jsonify({"status": "received"}), 200
        
        # Process the incoming data
        data = request.json  # This will parse the JSON payload
        print("Received Webhook Event:", data)

        return acknowledgement_response  # Return the acknowledgement response

if __name__ == '__main__':
    app.run(port=5000, debug=True)
