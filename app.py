from flask import Flask, request, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            user_id TEXT PRIMARY KEY,
            key TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            key_hash TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Simple API key auth (replace with your actual key)
API_KEY = "your-secure-api-key-here"

def validate_api_key():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return False
    provided_key = auth_header.split(' ')[1]
    return provided_key == API_KEY

@app.route('/verify', methods=['POST'])
def verify_key():
    try:
        if not validate_api_key():
            return jsonify({"success": False, "message": "Invalid API key"}), 401

        if not request.is_json:
            return jsonify({"success": False, "message": "Request must be JSON"}), 400

        data = request.get_json()
        key = data.get('verification_code')
        user_id = data.get('user_id')

        if not key or not user_id:
            return jsonify({"success": False, "message": "Missing verification_code or user_id"}), 400

        conn = sqlite3.connect('keys.db')
        cursor = conn.cursor()
        cursor.execute('SELECT key FROM keys WHERE user_id = ?', (str(user_id),))
        result = cursor.fetchone()
        conn.close()

        if result and result[0] == key:
            # Delete used key
            conn = sqlite3.connect('keys.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM keys WHERE user_id = ?', (str(user_id),))
            conn.commit()
            conn.close()
            return jsonify({"success": True, "message": "Key verified successfully!"}), 200
        else:
            return jsonify({"success": False, "message": "Invalid or expired key"}), 400

    except Exception as e:
        app.logger.error(f"Error in /verify: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@app.route('/add_key', methods=['POST'])
def add_key():
    try:
        if not validate_api_key():
            return jsonify({"success": False, "message": "Invalid API key"}), 401

        data = request.get_json()
        user_id = data.get('user_id')
        key = data.get('verification_code')

        if not user_id or not key:
            return jsonify({"success": False, "message": "Missing user_id or verification_code"}), 400

        conn = sqlite3.connect('keys.db')
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO keys (user_id, key) VALUES (?, ?)', (str(user_id), key))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Key added successfully"}), 200

    except Exception as e:
        app.logger.error(f"Error in /add_key: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
