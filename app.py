from flask import Flask, request, jsonify
import requests
import threading
import random
import time
import os
import json

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
current_leader_ip = ''

# Lista de nodos en el clúster (direcciones IP privadas)
peers = []

# Temporizador para la elección
election_timer = None

#Log persistente de cada instancia
log_file = 'log.json'
log = []

# Archivo de base de datos persistente
database_file = 'database.json'
database = {}

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

# Funcion para cargar los peers del archivo persistente
def load_peers(file_path):
    peers = []
    try:
        with open(file_path, 'r') as f:
            peers = [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Error al leer el archivo de peers: {e}")
    return peers

# Función para cargar el log desde el archivo persistente
def load_log():
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return json.load(f)
    else:
        return []
    
# Función para guardar el log en el archivo persistente
def save_log(log):
    with open(log_file, 'w') as f:
        json.dump(log, f, indent=4)

# Función para agregar entradas al log
def append_to_log(entry):
    log.append(entry)
    save_log(log)  # Guardar el log actualizado en el archivo

# Función para replicar el log en los followers y actualizar la base de datos
def replicate_to_followers(entry):
    success_count = 1  # El líder ya tiene la entrada replicada
    for peer in peers:
        try:
            response = requests.post(f"{peer}/append_entries", json=entry)
            if response.status_code == 200:
                success_count += 1
                print(f"Entrada replicada en {peer}")
        except Exception as e:
            print(f"Error replicando entrada en {peer}: {e}")

    if success_count > len(peers) // 2:
        print("Replicación exitosa en la mayoría de los nodos. Actualizando database.json")
        update_database(entry)
        for peer in peers:
            try:
                response = requests.post(f"{peer}/update_database", json=entry)
            except Exception as e:
                print(f"Error replicando entrada en {peer}: {e}")

# Función para sincronizar el log faltante
def sync_log_with_leader():
    if state == STATE_FOLLOWER:
        try:
            response = requests.get(f"http://{current_leader_ip}/get_log")
            leader_log = response.json()
            
            # Comparar y añadir entradas faltantes
            missing_entries = [entry for entry in leader_log if entry['index'] > len(log)]
            log.extend(missing_entries)
            
            save_log(log)  # Guardar el log sincronizado en el archivo persistente
            
            if missing_entries :
                print("Log sincronizado con el líder")
            else:
                print("No había nada que sincronizar")
        except Exception as e:
            print(f"Error al sincronizar log con el líder: {e}")

def on_reconnection():
    if state == STATE_FOLLOWER and current_leader_ip != '':
        sync_log_with_leader()

# Función para cargar la base de datos desde el archivo persistente
def load_database():
    if os.path.exists(database_file):
        with open(database_file, 'r') as f:
            return json.load(f)
    else:
        return {}

# Función para guardar la base de datos en el archivo persistente
def save_database():
    with open(database_file, 'w') as f:
        json.dump(database, f, indent=4)

# Función para agregar una entrada en la base de datos
def update_database(entry):
    database[entry['index']] = entry['message']
    save_database()

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
    global state, current_term, current_leader_ip
    data = request.json
    term = data['term']
    
    if term >= current_term:
        current_term = term
        state = STATE_FOLLOWER  # Si recibe un heartbeat, sigue como follower
        current_leader_ip = request.remote_addr  # Guardar la IP del líder
        print(f"IP del lider actual: {current_leader_ip}")
        reset_election_timer()  # Reiniciar el temporizador para evitar convertirse en candidato

    return jsonify({"status": "ok"})

# Endpoint para recibir operaciones de escritura
@app.route('/write', methods=['POST'])
def handle_write():
    global state

    if state != STATE_LEADER:
        return jsonify({"error": "No soy el líder"}), 403

    data = request.json
    message = data.get('message')

    # Crear nueva entrada de log
    new_entry = {"index": len(log) + 1, "operation": "write", "message": message}
    append_to_log(new_entry)  # Guardar en el archivo log.json

    # Replicar la nueva entrada en los followers
    replicate_to_followers(new_entry)

    return jsonify({"status": "ok", "entry": new_entry})

# Endpoint en los followers para recibir entradas de log replicadas
@app.route('/append_entries', methods=['POST'])
def handle_append_entries():
    entry = request.json
    log.append(entry)  # Agregar la nueva entrada al log en memoria
    save_log(log)  # Guardar el log actualizado en el archivo persistente

    return jsonify({"status": "ok"})

# Endpoint en los followers para recibir confirmación de cambiar la base de datos
@app.route('/update_database', methods=['POST'])
def handle_append_entries():
    entry = request.json
    update_database(entry)

    return jsonify({"status": "ok"})

# Endpoint en el líder para devolver su log completo
@app.route('/get_log', methods=['GET'])
def get_log():
    log = load_log()  # Asegurarse de leer siempre el archivo más actualizado
    return jsonify(log)

# Endpoint para obtener el estado actual del nodo
@app.route('/current_state', methods=['GET'])
def get_current_state():
    return jsonify({"current_state": state})

if __name__ == '__main__':
    # Iniciar el servidor Flask en un hilo separado
    server_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=80))
    server_thread.start()

    # Agregar un pequeño retardo antes de iniciar el temporizador de elección
    time.sleep(7)

    #Cargar los peers
    peers = load_peers('peers.txt')
    print(f"Peers cargados: {peers}")

    #Cargar el log y la database
    log = load_log()
    database = load_database()

    #Intentar obtener el log actualizado
    on_reconnection()

    print("Timeout para la elección:", election_timeout)
    reset_election_timer()

