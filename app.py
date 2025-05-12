from flask import Flask, request
import json

app = Flask(__name__)

# Simulate a database of verification codes
verification_codes = {}

@app.route('/verify', methods=['GET'])
def verify():
    code = request.args.get('code')
    
    if code in verification_codes:
        username = verification_codes[code]
        del verification_codes[code]  # Remove the code after it's used
        return json.dumps({"status": "verified", "username": username}), 200
    else:
        return json.dumps({"status": "not_verified"}), 400

@app.route('/store_code', methods=['POST'])
def store_code():
    data = request.json
    verification_codes[data['code']] = data['username']
    return json.dumps({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)
