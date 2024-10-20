from flask import Flask, request, jsonify

app = Flask(__name__)

# Finnhub Webhook Route - Allow both POST and GET methods
@app.route('/finnhub-webhook', methods=['POST', 'GET'])
def finnhub_webhook():
    # For GET requests, you might want to return a simple message
    if request.method == 'GET':
        return jsonify({"message": "Webhook is active and ready to receive POST requests."}), 200

    # For POST requests, process the incoming data
    if request.method == 'POST':
        headers = request.headers

        # Verify secret key (if you're using it)
        if headers.get('X-Finnhub-Secret') != 'csamt3pr01qobflkbj30':
            return jsonify({"error": "Invalid secret key"}), 403

        # Process the incoming data
        data = request.json
        print("Received Webhook Event:", data)

        # Return a 200 status code to acknowledge receipt
        return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
