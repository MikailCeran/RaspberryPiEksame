import socket
import json
import time
import base64
import pyaudio
from flask import Flask, request, jsonify
from threading import Thread

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
    # Start a separate thread to listen for socket data
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 9090))  # Use a different port for the socket

    print("Socket listener started on port 9090")

    while True:
        # Receive and process socket data
        data, addr = server_socket.recvfrom(1024)
        try:
            raw_data = data.decode()
            print(f"Raw data received from {addr}: {raw_data}")

            json_data = json.loads(raw_data)
            audio_data = json_data.get('audio_data')
            recorded_data.append(audio_data)
            print(f"Received audio data from {addr}")
        except json.JSONDecodeError:
            print("Invalid JSON format received")

def send_audio_data():
    # Function to send audio data every 10 seconds
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 9090)  # Change this to the server's IP and port

    # Set up PyAudio
    p = pyaudio.PyAudio()
    chunk_size = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk_size,
                    input=True)

    while True:
        # Read audio data from the microphone
        data = stream.read(chunk_size)

        # Convert the data to base64-encoded string
        audio_data = {'audio_data': base64.b64encode(data).decode()}

        # Convert the data to JSON format
        json_data = json.dumps(audio_data).encode()

        # Send the data to the server
        client_socket.sendto(json_data, server_address)

        print("Sent audio data")

        time.sleep(10)

    # Stop and close the PyAudio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    # Use '0.0.0.0' to listen on all public IPs
    app_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080, 'threaded': True})
    app_thread.start()

    # Start the socket listener in a separate thread
    socket_thread = Thread(target=start_socket_listener)
    socket_thread.start()

    # Start the function to send audio data in a separate thread
    audio_thread = Thread(target=send_audio_data)
    audio_thread.start()
