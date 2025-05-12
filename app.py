from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    roblox_user_id = str(data.get("user_id"))
    submitted_key = data.get("verification_code")

    with open("keys.json", "r") as f:
        keys = json.load(f)

    for discord_id, entry in keys.items():
        if entry["key"] == submitted_key and not entry.get("verified"):
            entry["verified"] = True
            with open("keys.json", "w") as f:
                json.dump(keys, f)
            return jsonify({"success": True})

    return jsonify({"success": False})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
