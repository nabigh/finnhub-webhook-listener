from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
SECRET_KEY = 'csamt3pr01qobflkbj30'

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/finnhub-webhook', methods=['POST'])
def receive_symbols():
    data = request.get_json()
    logging.info(f"Received data: {data}")

    # Validate the secret key
    if data.get('secret') != SECRET_KEY:
        return jsonify({'error': 'Invalid secret key'}), 403

    # Extract stock symbols
    symbols = data.get('symbols', [])
    logging.info(f"Processing symbols: {symbols}")

    # Here you can add logic to store symbols or process further
    # For now, we'll just print them
    print(f"Processed Symbols: {symbols}")

    return jsonify({'message': 'Symbols processed successfully!', 'symbols': symbols}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
