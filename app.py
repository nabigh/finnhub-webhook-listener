from flask import Flask, request, jsonify

app = Flask(__name__)

# Finnhub Webhook Route - Ensure POST method is specified
@app.route('/finnhub-webhook', methods=['POST'])
def finnhub_webhook():
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
