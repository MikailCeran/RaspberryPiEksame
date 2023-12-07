import numpy as np
import soundfile as sf
from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes of the Flask app

def calculate_decibels(audio_data):
    # Your decibel calculation logic here
    # This is a basic example using the mean of the absolute values
    decibels = 20 * np.log10(np.mean(np.abs(audio_data)))
    return decibels

def capture_audio():
    duration = 1  # seconds
    samplerate = 44100

    audio_data = np.random.random(samplerate * duration)  # Replace this with your actual audio capture logic

    return audio_data

@app.route('/get_decibels', methods=['GET'])
def get_decibels():
    audio_data = capture_audio()
    decibels = calculate_decibels(audio_data)
    return jsonify({"decibels": decibels})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
