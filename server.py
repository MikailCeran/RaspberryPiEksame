import socket
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

recorded_data = []

@app.route('/record', methods=['POST'])
def record_data():
    data = request.get_json()
    decibel_data = data.get('decibel_data')

    # Store decibel data (this is a simplified example)
    recorded_data.append(decibel_data)

    return jsonify({'status': 'success'})

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify({'recorded_data': recorded_data})

def start_socket_listener():
    # Start a separate thread or process to listen for socket data
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9090))  # Use a different port for the socket
    server_socket.listen(1)

    print("Socket listener started on port 9090")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        
        # Receive and process socket data
        data = client_socket.recv(1024)
        try:
            json_data = json.loads(data.decode())
            decibel_data = json_data.get('decibel_data')
            recorded_data.append(decibel_data)
            print(f"Received data from socket: {decibel_data}")
            client_socket.send(b"Data received successfully")
        except json.JSONDecodeError:
            print("Invalid JSON format received")

        client_socket.close()

if __name__ == '__main__':
    # Use '0.0.0.0' to listen on all public IPs
    app.run(host='0.0.0.0', port=8080, threaded=True)

    # Start the socket listener in a separate thread
    import threading
    socket_thread = threading.Thread(target=start_socket_listener)
    socket_thread.start()
