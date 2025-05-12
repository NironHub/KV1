from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('verification.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS verifications (user_id INTEGER PRIMARY KEY, verification_code TEXT)")
conn.commit()

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    user_id = data.get("user_id")
    verification_code = data.get("verification_code")

    cursor.execute("SELECT verification_code FROM verifications WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row and row[0] == verification_code:
        return jsonify({"success": True})
    return jsonify({"success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
