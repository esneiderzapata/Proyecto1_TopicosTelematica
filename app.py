from flask import Flask, request, jsonify
import requests
import threading
import random
import time

app = Flask(__name__)

# Estados del nodo
STATE_FOLLOWER = 'follower'
STATE_CANDIDATE = 'candidate'
STATE_LEADER = 'leader'

# Variables de estado del nodo
current_term = 0         # El término actual (aumenta con cada elección)
voted_for = None          # A quién votó este nodo en este término
state = STATE_FOLLOWER    # Estado inicial
votes_received = 0        # Votos recibidos en esta elección
election_timeout = random.uniform(3, 5)  # Tiempo aleatorio antes de empezar una elección

# Lista de nodos en el clúster (direcciones IP privadas)
peers = ['http://172.31.38.10', 'http://172.31.36.31', 'http://172.31.43.43']

# Temporizador para la elección
election_timer = None

# Función para reiniciar el temporizador de elección
def reset_election_timer():
    global election_timer
    if election_timer:
        election_timer.cancel()
    election_timer = threading.Timer(election_timeout, start_election)
    election_timer.start()

# Función para iniciar una elección
def start_election():
    global state, current_term, votes_received, voted_for
    state = STATE_CANDIDATE
    current_term += 1
    votes_received = 1  # El nodo se vota a sí mismo
    voted_for = 'self'
    
    print(f"Iniciando elección. Término actual: {current_term}")
    
    # Enviar solicitudes de voto a los demás nodos
    for peer in peers:
        threading.Thread(target=request_vote, args=(peer,)).start()

# Función para solicitar un voto de otro nodo
def request_vote(peer):
    print("Solicitando voto a: ", peer)
    global current_term
    try:
        response = requests.post(f"{peer}/request_vote", json={"term": current_term})
        if response.status_code == 200:
            result = response.json()
            if result['vote_granted']:
                print(f"Voto de {peer} recibido")
                global votes_received
                votes_received += 1
                if votes_received > len(peers) // 2 and state == STATE_CANDIDATE:
                    become_leader()
            else:
                print(f"Voto de {peer} denegado")
    except Exception as e:
        print(f"Error solicitando voto de {peer}: {e}")

# Función para convertirse en líder
def become_leader():
    global state
    state = STATE_LEADER
    print("Se ha elegido un nuevo líder!")
    # Empezar a enviar heartbeats a los followers
    threading.Thread(target=send_heartbeats).start()

# Función para enviar heartbeats a los followers
def send_heartbeats():
    global state
    while state == STATE_LEADER:
        for peer in peers:
            try:
                requests.post(f"{peer}/heartbeat", json={"term": current_term})
                print("Latido enviado a", peer)
            except Exception as e:
                print(f"Error enviando heartbeat a {peer}: {e}")
        time.sleep(1)  # Enviar heartbeats cada segundo

def get_private_ip():
    try:
        response = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4')
        private_ip = response.text
        return private_ip
    except Exception as e:
        print(f"Error al obtener la IP privada: {e}")
        return "No se ha recibido la IP"


# Endpoint para recibir solicitudes de voto
@app.route('/request_vote', methods=['POST'])
def handle_request_vote():
    global current_term, voted_for
    data = request.json
    term = data['term']

    if term > current_term:
        current_term = term
        voted_for = None

    if voted_for is None:
        voted_for = request.remote_addr
        reset_election_timer()  # Reiniciar temporizador si vota por alguien
        return jsonify({"vote_granted": True})
    else:
        return jsonify({"vote_granted": False})

# Endpoint para recibir heartbeats
@app.route('/heartbeat', methods=['POST'])
def handle_heartbeat():
    global state, current_term
    data = request.json
    term = data['term']

    if term >= current_term:
        current_term = term
        state = STATE_FOLLOWER  # Si recibe un heartbeat, sigue como follower
        reset_election_timer()  # Reiniciar el temporizador para evitar convertirse en candidato

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # Iniciar el servidor Flask en un hilo separado
    server_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=80))
    server_thread.start()
    
    # Agregar un pequeño retardo antes de iniciar el temporizador de elección
    time.sleep(7)
    print("Timeout para la elección:", election_timeout)
    get_private_ip()
    reset_election_timer()

