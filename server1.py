import socket
import json
import time
import base64
import pyaudio
from flask import Flask, request, jsonify
from threading import Thread

app = Flask(__name__)

recorded_data = []
data_file_path = 'recorded_data.txt'
max_entries = 20

def save_data_to_file(data):
    with open(data_file_path, 'a') as file:
        file.write(json.dumps(data) + '\n')

def check_data_file_size():
    try:
        file_size = os.path.getsize(data_file_path)
        if file_size > 1024 * 1024:  # Check if file size exceeds 1MB
            with open(data_file_path, 'w') as file:
                file.write('')
            print('Data file truncated due to size limit.')
    except FileNotFoundError:
        pass

@app.route('/record', methods=['POST'])
def record_data():
    # Use PyAudio to capture audio data
    decibel_data = capture_decibels()

    # Store decibel data
    recorded_data.append(decibel_data)
    save_data_to_file({'decibel_data': decibel_data})

    # Check the number of entries and file size
    if len(recorded_data) > max_entries:
        recorded_data.pop(0)  # Remove the oldest entry
    check_data_file_size()

    return jsonify({'status': 'success'})

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify({'recorded_data': recorded_data})

def capture_decibels():
    # Use PyAudio to capture audio data
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

    # Read audio data from the microphone
    data = stream.read(chunk_size)

    # Stop and close the PyAudio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert the data to base64-encoded string
    audio_data = {'audio_data': base64.b64encode(data).decode()}

    # Convert the data to JSON format
    json_data = json.dumps(audio_data).encode()

    return json_data

def send_audio_data():
    # Function to send audio data every 10 seconds
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('192.168.50.236', 9090)  # Replace with the IP address of the machine running the listener

    while True:
        # Capture and send audio data
        audio_data = capture_decibels()
        client_socket.sendto(audio_data, server_address)

        print("Sent audio data")

        time.sleep(10)

if __name__ == '__main__':
    # Use '0.0.0.0' to listen on all public IPs
    app_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080, 'threaded': True})
    app_thread.start()

    # Start the function to send audio data in a separate thread
    audio_thread = Thread(target=send_audio_data)
    audio_thread.start()
