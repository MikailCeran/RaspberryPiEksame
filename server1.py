# server1.py
from flask import Flask, jsonify, send_file
from flask_cors import CORS
import json
import os
import numpy as np
import pyaudio

app = Flask(__name__)
CORS(app)

# Route to get decibel data directly from the JSON file
@app.route('/get_decibels_data', methods=['GET'])
def get_decibels_data():
    try:
        with open('decibels_data.json', 'r') as json_file:
            decibels_data = json.load(json_file)
        return jsonify(decibels_data)
    except Exception as e:
        return jsonify({"error": str(e)})

# Route for the index page
@app.route('/')
def index():
    return "Hello, this is the index page!"

# Route to get decibels using the previous logic
@app.route('/get_decibels', methods=['GET'])
def get_decibels():
    from tasks.tasks import calculate_and_send_decibels
    try:
        audio_data = capture_audio()
        decibels = calculate_and_send_decibels(audio_data)
        return jsonify({"decibels": decibels["decibels"]})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to get captured audio file
@app.route('/captured_audio', methods=['GET'])
def get_captured_audio():
    try:
        return send_file('captured_audio.wav', as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})

# Function to capture audio from the microphone using PyAudio
def capture_audio():
    try:
        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Set the sampling parameters
        duration = 1  # seconds
        samplerate = 44100
        channels = 1  # 1 for mono, 2 for stereo

        # Open a stream for audio input
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=samplerate,
                        input=True,
                        frames_per_buffer=samplerate)

        # Read audio data from the stream
        frames = []
        for i in range(int(samplerate / duration)):
            data = stream.read(int(samplerate * duration / (samplerate / duration)))
            frames.append(np.frombuffer(data, dtype=np.int16))

        # Close the stream
        stream.stop_stream()
        stream.close()

        # Convert the frames to a NumPy array
        audio_data = np.concatenate(frames)

        return audio_data

    except Exception as e:
        return {"error": str(e)}
    finally:
        # Terminate the PyAudio instance
        p.terminate()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
