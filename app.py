from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulate the storage of keys (you should use a real database in production)
keys_db = {}

@app.route('/verify', methods=['POST'])
def verify_key():
    try:
        # Get the data sent by the Roblox game
        data = request.get_json()

        # Debug: Print received data for troubleshooting
        print(f"Received data: {data}")

        # Ensure that 'verification_code' and 'user_id' exist in the data
        key = data.get('verification_code')
        user_id = data.get('user_id')

        # If key or user_id are missing, return an error response
        if not key or not user_id:
            print("Missing verification_code or user_id.")  # Debug log
            return jsonify({"success": False, "message": "Missing verification_code or user_id."}), 400

        # Check if the key is valid (match user_id with stored key)
        if str(user_id) in keys_db and keys_db[str(user_id)] == key:
            # Key is valid, proceed with verification
            del keys_db[str(user_id)]  # Optionally remove the key after verification
            print(f"Key for user {user_id} verified successfully.")  # Debug log
            return jsonify({"success": True, "message": "Key verified successfully!"}), 200
        else:
            print("Invalid or expired key.")  # Debug log
            return jsonify({"success": False, "message": "Invalid or expired key."}), 400

    except Exception as e:
        # Print detailed error message
        print(f"Error: {str(e)}")  # Print the exact error for debugging
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500

# Route to manually add keys (for testing purposes)
@app.route('/add_key', methods=['POST'])
def add_key():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        key = data.get('verification_code')

        if user_id and key:
            keys_db[str(user_id)] = key
            print(f"Added key for user {user_id}: {key}")  # Debug log
            return jsonify({"success": True, "message": "Key added successfully."}), 200
        else:
            print("Missing user_id or verification_code.")  # Debug log
            return jsonify({"success": False, "message": "Missing user_id or verification_code."}), 400
    except Exception as e:
        print(f"Error: {str(e)}")  # Print the exact error for debugging
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
