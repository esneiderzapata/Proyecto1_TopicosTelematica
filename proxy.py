from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

NODES_IP = ["http://172.31.38.10", "http://172.31.36.31", "http://172.31.43.43"]  # List of nodes

@app.route('/write', methods=['POST'])
def handle_write():
    data = request.json
    leader_url = None
    # Forward the write request to the leader
    for ip in NODES_IP:
        try:
            temp = requests.get(f"{ip}/current_state")
            
            if temp.json().get("current_state") == "leader":
                leader_url = ip
                break
        except Exception as e:
            print(f"Error al verificar estado en {ip}: {e}")
    
    if leader_url:
        response = requests.post(f"{leader_url}/write", json=data)
        return jsonify({
            "response": response.json(),
            "leader_ip": leader_url
        })
    else:
        return jsonify({"error": "No leader found"}), 500

@app.route('/read', methods=['GET'])
def handle_read():
    # Forward the read request to one of the followers (can be randomized)
    followers = []
    petition = random.randint(0, 1)
    
    for ip in NODES_IP:
        try:
            temp = requests.get(f"{ip}/current_state")
            if temp.json().get("current_state") == "follower":
                followers.append(ip)
        except Exception as e:
            print(f"Error al verificar estado en {ip}: {e}")
    
    if followers:
        follower_ip = followers[petition]
        response = requests.get(f"{follower_ip}/read")  # Could rotate between followers
        return jsonify({
            "response": response.json(),
            "follower_ip": follower_ip
        })
    else:
        return jsonify({"error": "No followers available"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

