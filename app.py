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
    
    # Log all other headers
    for header, value in request.headers:
        print(f"{header}: {value}")
    
    # Log content-type and content-length if they exist
    if 'Content-Type' in request.headers:
        print(f"Content-Type: {request.headers['Content-Type']}")
    if 'Content-Length' in request.headers:
        print(f"Content-Length: {request.headers['Content-Length']}")
    
    # Log the body of the request
    print("\n" + request.get_data(as_text=True))

    # Check if the content-type is supported (JSON or plain text)
    if request.content_type not in ['application/json', 'text/plain']:
        return jsonify({"error": "Unsupported Media Type"}), 415
    
    # Get the X-Finnhub-Secret header from the request
    request_secret = request.headers.get('X-Finnhub-Secret')

    # Verify if the secret key matches
    if request_secret != FINNHUB_SECRET:
        return jsonify({"error": "Unauthorized request"}), 403
    
    # Acknowledge the webhook event
    acknowledgment_response = jsonify({"status": "received"}), 200

    # Handle both JSON and text payloads
    if request.content_type == 'application/json':
        event_data = request.json
    else:
        event_data = request.get_data(as_text=True)

    # Process and log the event data
    print(f"\nParsed Event Data: {event_data}")
    
    return acknowledgment_response

if __name__ == '__main__':
    app.run(debug=True)
