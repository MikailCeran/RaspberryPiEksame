import requests
import numpy as np

# Replace this URL with your Azure web app URL
api_url = "https://restnoise.azurewebsites.net/api/noise"

def generate_random_audio_data():
    # Simulate capturing audio by generating random decibel values
    return np.random.uniform(low=30, high=80, size=44100).tolist()

def send_audio_data_to_server(audio_data):
    try:
        response = requests.post(api_url, json={"audio_data": audio_data})
        response.raise_for_status()
        print("Audio data sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending audio data: {e}")

if __name__ == "__main__":
    # Generate random audio data
    audio_data = generate_random_audio_data()

    # Send audio data to the Flask API
    send_audio_data_to_server(audio_data)
