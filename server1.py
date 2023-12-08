# server1.py
from flask import Flask, jsonify, send_file
from flask_cors import CORS
import json
import numpy as np
import pyaudio
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

# Route to get decibel data directly from the JSON file
@app.route('/get_decibels_data', methods=['GET'])
def get_decibels_data():
    try:
        with lock:
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
        with lock:
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

# Periodic task to calculate average decibels every 1 minute
def calculate_average_decibels_1min():
    global decibel_readings, decibels_data

    with lock:
        try:
            # Capture audio data
            audio_data = capture_audio()

            # Calculate the average decibel level for the past 1 minute
            average_decibel = np.mean(audio_data)

            # Store the average and timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            decibel_readings.append((average_decibel, timestamp))

            # Trim the list to keep only the last 10 minutes of readings
            decibel_readings = decibel_readings[-10:]

            # Update the JSON file
            decibels_data["average_pr_1min"] = [(average_decibel, timestamp)]
            with open('decibels_data.json', 'w') as json_file:
                json.dump(decibels_data, json_file)

        except Exception as e:
            print(f"Error in calculate_average_decibels_1min: {e}")

    # Schedule the task to run again in 1 minute
    threading.Timer(60, calculate_average_decibels_1min).start()

# Periodic task to calculate average decibels every 10 minutes
def calculate_average_decibels_10min():
    global decibel_readings, decibels_data

    with lock:
        try:
            # Calculate the average decibel level for the past 10 minutes
            if decibel_readings:
                average_10min = np.mean([reading[0] for reading in decibel_readings])
                decibels_data["average_pr_10min"].append((average_10min, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                # Trim the list to keep only the last 10 minutes of readings
                decibel_readings = decibel_readings[-10:]

                # Update the JSON file
                with open('decibels_data.json', 'w') as json_file:
                    json.dump(decibels_data, json_file)

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
