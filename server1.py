import socket
import json
import time
import base64
import pyaudio
from flask import Flask, jsonify
from threading import Thread
from soundmeter import Meter

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
    # Use soundmeter to capture decibel data
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
    # Use soundmeter to capture decibel data
    meter = Meter(device='default', dBA=True, stream=True)
    decibel_data = meter.get()

    return decibel_data

def send_data():
    # Function to send decibel data every 10 seconds
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('192.168.50.236', 9090)  # Replace with the IP address of the machine running the listener

    while True:
        # Use soundmeter to capture decibel data
        decibel_data = capture_decibels()

        # Convert the data to JSON format
        data = {'decibel_data': decibel_data}
        json_data = json.dumps(data).encode()

        # Send the data to the server
        client_socket.sendto(json_data, server_address)

        print("Sent decibel data")

        time.sleep(10)

if __name__ == '__main__':
    # Use '0.0.0.0' to listen on all public IPs
    app_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080, 'threaded': True})
    app_thread.start()

    # Start the function to send decibel data in a separate thread
    data_thread = Thread(target=send_data)
    data_thread.start()
