from flask import Flask, request, jsonify

app = Flask(__name__)

# Secret key for validation
SECRET_KEY = 'csamt3pr01qobflkbj30'

@app.route('/finnhub-webhook', methods=['POST'])
def receive_symbols():
    data = request.get_json()
    print(f"Received data: {data}")  # Log the received data for debugging

    # Check the secret key for validation
    if data.get('secret') != SECRET_KEY:
        return jsonify({'error': 'Invalid secret key'}), 403

    # Process the symbols
    symbols = data.get('symbols', [])
    # Here you would add logic to process the symbols with Finnhub
    print(f"Processing symbols: {symbols}")

    # Return success message
    return jsonify({'message': 'Symbols received successfully!'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # Change port if needed
