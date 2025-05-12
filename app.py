import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the keys from a JSON file (keys.json should exist on the server)
def load_keys():
    try:
        with open("keys.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("keys.json not found!")
        return None

@app.route("/verify", methods=["POST"])
def verify_key():
    # Get the posted data
    data = request.get_json()
    if not data or "key" not in data:
        return jsonify({"error": "No key provided"}), 400

    user_key = data["key"]
    keys = load_keys()

    if keys is None:
        return jsonify({"error": "Failed to load keys"}), 500

    if user_key in keys:
        # If the key exists in keys.json, send confirmation
        return jsonify({"status": "success", "message": "Verification successful!"}), 200
    else:
        # If key doesn't match, return error
        return jsonify({"status": "failure", "message": "Invalid key!"}), 400

if __name__ == "__main__":
    app.run(debug=True)
