from flask import Flask, jsonify
import requests
import threading
import time
import os

app = Flask(__name__)
url = os.getenv("CHECK_URL")
if not url:
    raise ValueError("The CHECK_URL environment variable is not set.")

server_status = {"alive": False}

def check_server_status():
    global server_status
    while True:
        try:
            response = requests.get(url)
            data = response.json()
            server_status["alive"] = data.get("code") == 200 and data.get("msg") == "working"
        except (requests.RequestException, ValueError):
            server_status["alive"] = False
        time.sleep(60)

@app.route('/check', methods=['GET'])
def check():
    return jsonify(server_status)

if __name__ == '__main__':
    threading.Thread(target=check_server_status, daemon=True).start()
    app.run(debug=True, port=5000)
