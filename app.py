from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the secret key for verifying Finnhub webhook requests
FINNHUB_SECRET = 'csamt3pr01qobflkbj30'

# Route for handling Finnhub webhooks
@app.route('/finnhub-webhook', methods=['POST'])
def finnhub_webhook():
    # Log the request method, path, and protocol
    print(f"{request.method} {request.path} {request.environ.get('SERVER_PROTOCOL')}")

    # Log the host header
    print(f"Host: {request.host}")

    # Log all headers
    for header, value in request.headers:
        print(f"{header}: {value}")

    # Log the body of the request
    body = request.get_data(as_text=True)
    print("\nRequest Body:")
    print(body)

    # Check if Content-Type is present
    content_type = request.headers.get('Content-Type')
    print(f"Content-Type: {content_type}")

    # Verify if the content-type is application/json
    if content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    # Get the X-Finnhub-Secret header from the request
    request_secret = request.headers.get('X-Finnhub-Secret')

    # Verify if the secret key matches
    if request_secret != FINNHUB_SECRET:
        return jsonify({"error": "Unauthorized request"}), 403

    # Process the JSON data
    event_data = request.json

    # Log the parsed event data
    print("\nParsed Event Data:")
    print(event_data)

    # Acknowledge the webhook event
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(debug=True)
