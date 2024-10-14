from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

LEADER_URL = "http://leader-server-url"
FOLLOWER_URLS = ["http://follower1-url", "http://follower2-url"]  # List of followers

@app.route('/write', methods=['POST'])
def handle_write():
    data = request.json
    # Forward the write request to the leader
    #Leader url will be by a method for getting the leader ip
    response = requests.post(f"{LEADER_URL}/write", json=data)
    return response.text

@app.route('/read', methods=['GET'])
def handle_read():
    # Forward the read request to one of the followers (can be randomized)
    # Same to this method the url will be given by a method in ap[p.py]
    response = requests.get(f"{FOLLOWER_URLS[0]}/read")  # Could rotate between followers
    return response.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)