from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Simulate the storage of keys sent by the bot (this can be a database in a production system)
keys_db = {}

@app.route('/verify', methods=['POST'])
def verify():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        key = data.get("key")

        # Validate the key
        if key in keys_db.values():
            # Key is valid, return success
            user_id = list(keys_db.keys())[list(keys_db.values()).index(key)]
            # After verification, you can clear the key (or flag it as verified in your db)
            del keys_db[user_id]  # or set verified flag
            return jsonify({"status": "success", "message": "Key is valid. User has been verified."}), 200
        else:
            # Invalid key
            return jsonify({"status": "failed", "message": "Invalid or expired key."}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Example route to add a key manually (useful for testing)
@app.route('/add_key', methods=['POST'])
def add_key():
    data = request.get_json()
    user_id = data.get("user_id")
    key = data.get("key")
    
    if user_id and key:
        keys_db[user_id] = key
        return jsonify({"status": "success", "message": "Key added successfully."}), 200
    else:
        return jsonify({"status": "failed", "message": "Missing user_id or key."}), 400

if __name__ == '__main__':
    app.run(debug=True)
