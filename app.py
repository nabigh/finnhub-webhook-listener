from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the secret key for verifying Finnhub webhook requests
FINNHUB_SECRET = 'csamt3pr01qobflkbj30'

# Route for handling Finnhub webhooks
@app.route('/finnhub-webhook', methods=['POST'])
def finnhub_webhook():
    # Check the Content-Type to ensure it's JSON
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415
    
    # Get the X-Finnhub-Secret header from the request
    request_secret = request.headers.get('X-Finnhub-Secret')
    
    # Verify if the secret key matches
    if request_secret != FINNHUB_SECRET:
        return jsonify({"error": "Unauthorized request"}), 403
    
    # Immediately send a 200 acknowledgment to prevent webhook disablement
    acknowledgment_response = jsonify({"status": "received"}), 200
    
    # Retrieve and process the event data
    event_data = request.json
    print(f"Received Finnhub Webhook Event: {event_data}")
    
    # TODO: Add any specific logic to handle the webhook event here, such as updating trading algorithms
    
    return acknowledgment_response  # Respond with acknowledgment

if __name__ == '__main__':
    app.run(debug=True)
