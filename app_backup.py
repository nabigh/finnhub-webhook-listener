from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the secret key for verifying Finnhub webhook requests
FINNHUB_SECRET = 'csamt3pr01qobflkbj30'

# Route for handling Finnhub webhooks
@app.route('/finnhub-webhook', methods=['POST'])
def finnhub_webhook():
    # Log request headers and body for debugging
    print(f"Headers: {request.headers}")
    print(f"Body: {request.get_data(as_text=True)}")

    # Check if the content-type is supported (JSON or plain text)
    if request.content_type not in ['application/json', 'text/plain']:
        return jsonify({"error": "Unsupported Media Type"}), 415
    
    # Get the X-Finnhub-Secret header from the request
    request_secret = request.headers.get('X-Finnhub-Secret')

    # Verify if the secret key matches
    if request_secret != FINNHUB_SECRET:
        return jsonify({"error": "Unauthorized request"}), 403
    
    # Immediately send a 200 acknowledgment to prevent webhook disablement
    acknowledgment_response = jsonify({"status": "received"}), 200

    # Handle both JSON and text payloads
    if request.content_type == 'application/json':
        event_data = request.json
    else:
        event_data = request.get_data(as_text=True)

    # Log the received event data
    print(f"Received Finnhub Webhook Event: {event_data}")
    
    # TODO: Add specific logic to handle the webhook event data (e.g., trigger trades, log events)

    return acknowledgment_response

if __name__ == '__main__':
    app.run(debug=True)
