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
    #Leader url will be by a method for getting the leader ip http://{ip_de_la_instancia}/current_state
    for i in range(0,3,1):
        temp = requests.get(f"{NODES_IP[i]}/current_state")
        if temp["current_state"] == "leader":
            leader_url = NODES_IP[i]
            break
    response = requests.post(f"{leader_url}/write", json=data)
    return response.text

@app.route('/read', methods=['GET'])
def handle_read():
    # Forward the read request to one of the followers (can be randomized)
    follower  = []
    petition = random.randint(0,1)    
    for i in range(0,3,1):
        temp = requests.get(f"{NODES_IP[i]}/current_state")
        if temp["current_state"] == "follower":
            follower.append(NODES_IP[i])

    response = requests.get(f"{follower[petition]}/read")  # Could rotate between followers
    return response.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)