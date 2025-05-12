from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulate the storage of keys (in production, you should use a database)
keys_db = {}

# Route to handle key verification
@app.route('/verify', methods=['POST'])
def verify_key():
    try:
        # Get the JSON data sent by the Roblox game
        data = request.get_json()
        print(f"Received data: {data}")  # Debug: print received data

        # Extract key and user_id
        key = data.get('verification_code')
        user_id = data.get('user_id')

        # Debug: Check if the expected data is present
        if not key or not user_id:
            return jsonify({"success": False, "message": "Missing verification_code or user_id."}), 400

        # Check if the key is valid
        if user_id in keys_db and keys_db[user_id] == key:
            # Key is valid, proceed with verification
            del keys_db[user_id]  # Optionally remove the key after verification
            return jsonify({"success": True, "message": "Key verified successfully!"}), 200
        else:
            return jsonify({"success": False, "message": "Invalid or expired key."}), 400

    except Exception as e:
        print(f"Error: {e}")  # Debug: print the error that occurred
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500


# A test route to manually add keys (for testing purposes)
@app.route('/add_key', methods=['POST'])
def add_key():
    data = request.get_json()
    user_id = data.get('user_id')
    key = data.get('verification_code')

    if user_id and key:
        keys_db[user_id] = key
        return jsonify({"success": True, "message": "Key added successfully."}), 200
    else:
        return jsonify({"success": False, "message": "Missing user_id or verification_code."}), 400

if __name__ == '__main__':
    app.run(debug=True)
