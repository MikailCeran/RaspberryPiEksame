import requests
import numpy as np
import json
import time
import socketio

# Replace this URL with the actual Azure API endpoint
azure_api_host = "apirestnoise.azurewebsites.net"
azure_api_url = f"https://{azure_api_host}"

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

def capture_audio():
    # Simulate capturing audio by generating random decibel values
    return np.random.uniform(low=30, high=80, size=44100).tolist()  # Convert to list for JSON serialization

def upload_audio(audio_data):
    try:
        data = {"audio_data": audio_data}
        sio.emit("upload_audio", data)
        print("Audio data uploaded successfully")
    except Exception as e:
        print(f"Error uploading audio data: {e}")

def get_decibels_data():
    try:
        response = requests.get(f"{azure_api_url}/get_decibels_data")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error retrieving decibel data. Status code: {response.status_code}, Error: {response.text}")
            return None

    except Exception as e:
        print(f"Error retrieving decibel data: {e}")
        return None

if __name__ == "__main__":
    sio.connect(azure_api_url)

    while True:
        # Simulate capturing audio and uploading to the server
        audio_data = capture_audio()
        upload_audio(audio_data)

        # Retrieve and print decibel data from the server
        decibel_data = get_decibels_data()
        if decibel_data:
            print("Decibel Data:", decibel_data)

        # Sleep for a minute before capturing/uploading again
        time.sleep(60)
