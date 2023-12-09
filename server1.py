from flask import Flask, jsonify, send_file
from flask_cors import CORS
import json
import numpy as np
import sounddevice as sd
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
CORS(app)

# Global variables for storing decibel readings and timestamps
decibel_readings = []
decibels_data = {"average_pr_1min": [], "average_pr_10min": []}

# Lock for thread safety when updating global variables
lock = threading.Lock()

def capture_audio():
    try:
        # Set the sampling parameters
        duration = 1  # seconds
        samplerate = 44100
        channels = 1  # 1 for mono, 2 for stereo

        # Record audio data from the microphone
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype=np.int16)
        sd.wait()

        return audio_data.flatten()

    except Exception as e:
        print(f"Error in capture_audio: {e}")
        return {"error": str(e)}

# Route to get decibel data directly from the JSON file
@app.route('/get_decibels_data', methods=['GET'])
def get_decibels_data():
    try:
        with lock:
            return jsonify(decibels_data)
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to get captured audio file
@app.route('/captured_audio', methods=['GET'])
def get_captured_audio():
    try:
        return send_file('captured_audio.wav', as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})

# Periodic task to calculate average decibels every 1 minute
def calculate_average_decibels_1min():
    global decibels_data

    try:
        # Capture audio data
        audio_data = capture_audio()

        # Calculate the average decibel level for the past 1 minute
        average_decibel = np.mean(np.abs(audio_data))

        # Store the average and timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        decibels_data["average_pr_1min"] = [(average_decibel, timestamp)]

    except Exception as e:
        print(f"Error in calculate_average_decibels_1min: {e}")

    # Schedule the task to run again in 1 minute
    threading.Timer(60, calculate_average_decibels_1min).start()

# Periodic task to calculate average decibels every 10 minutes
def calculate_average_decibels_10min():
    global decibels_data

    try:
        # Calculate the average decibel level for the past 10 minutes
        if decibels_data["average_pr_1min"]:
            average_10min = np.mean([reading[0] for reading in decibels_data["average_pr_1min"]])
            decibels_data["average_pr_10min"].append((average_10min, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            # Trim the list to keep only the last 10 minutes of readings
            decibels_data["average_pr_1min"] = decibels_data["average_pr_1min"][-10:]

    except Exception as e:
        print(f"Error in calculate_average_decibels_10min: {e}")

    # Schedule the task to run again in 10 minutes
    threading.Timer(600, calculate_average_decibels_10min).start()

if __name__ == "__main__":
    # Start the threads for periodic tasks
    threading.Timer(60, calculate_average_decibels_1min).start()
    threading.Timer(600, calculate_average_decibels_10min).start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, threaded=True)
