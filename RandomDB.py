# Raspberry Pi - record_and_send.py
import sounddevice as sd
import requests
import json

def record_and_send():
    # Code to record audio using sounddevice (adjust parameters as needed)
    sample_rate = 44100
    duration = 5
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()

    # Convert audio data to decibels (this is a simplified example, you may need to adjust)
    decibel_data = calculate_decibels(audio_data)

    # Replace 'your_server_ip' with the actual IP address of your Flask server
    server_url = 'http://server_ip:8080/record'

    data = {"decibel_data": decibel_data.tolist()}  # Convert NumPy array to list
    response = requests.post(server_url, json=data)

    print(response.text)

def calculate_decibels(audio_data):
    # Implement your logic to convert audio data to decibels here
    # This is a simplified example, you may need to use a library like numpy
    return audio_data.mean()

record_and_send()
