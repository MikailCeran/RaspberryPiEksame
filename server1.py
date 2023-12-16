from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import numpy as np
import threading
import queue
import time
from datetime import datetime, timedelta
import pyaudio

app = Flask(__name__)
CORS(app)

decibels_data = {"average_pr_1min": [], "average_pr_10min": []}
lock = threading.Lock()
audio_queue = queue.Queue()

def capture_audio():
    # Simulate capturing audio by generating random decibel values
    return np.random.uniform(low=30, high=80, size=44100)  # Random values between 30 and 80

@app.route('/get_decibels_data', methods=['GET'])
def get_decibels_data():
    try:
        with lock:
            return jsonify(decibels_data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    try:
        data = request.json
        audio_data = np.array(data["audio_data"])
        # Process the audio data if needed
        audio_queue.put(audio_data)
        return jsonify({"message": "Audio data received successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/captured_audio', methods=['GET'])
def get_captured_audio():
    try:
        return send_file('captured_audio.wav', as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})

def calculate_average_decibels_1min():
    global decibels_data

    while True:
        try:
            audio_data = audio_queue.get()
            average_decibel = np.mean(np.abs(audio_data))
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with lock:
                decibels_data["average_pr_1min"] = [(average_decibel, timestamp)]

            print(f"1-minute average decibel: {average_decibel}")

        except Exception as e:
            print(f"Error in calculate_average_decibels_1min: {e}")

        time.sleep(60)

def calculate_average_decibels_10min():
    global decibels_data

    while True:
        try:
            if decibels_data["average_pr_1min"]:
                average_10min = np.mean([reading[0] for reading in decibels_data["average_pr_1min"]])
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                with lock:
                    decibels_data["average_pr_10min"].append((average_10min, timestamp))
                    decibels_data["average_pr_1min"] = decibels_data["average_pr_1min"][-10:]

                print(f"10-minute average decibel: {average_10min}")

        except Exception as e:
            print(f"Error in calculate_average_decibels_10min: {e}")

        time.sleep(600)

if __name__ == "__main__":
    threading.Thread(target=calculate_average_decibels_1min).start()
    threading.Thread(target=calculate_average_decibels_10min).start()

    app.run(host='0.0.0.0', port=8080, threaded=True)
