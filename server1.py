from flask import Flask, jsonify, send_file
from flask_cors import CORS
import numpy as np
import sounddevice as sd
from datetime import datetime, timedelta
import threading
import queue
import time  # Add this line to import the time module
import pyaudio

app = Flask(__name__)
CORS(app)

decibels_data = {"average_pr_1min": [], "average_pr_10min": []}
lock = threading.Lock()
audio_queue = queue.Queue()

def capture_audio():
    try:
        # Set the sampling parameters
        duration = 1  # seconds
        samplerate = 44100
        channels = 1  # 1 for mono, 2 for stereo

        # Record audio data from the default audio device
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype=np.int16)
        sd.wait()

        return audio_data.flatten()

    except Exception as e:
        print(f"Error in capture_audio: {e}")
        return {"error": str(e)}


@app.route('/get_decibels_data', methods=['GET'])
def get_decibels_data():
    try:
        with lock:
            return jsonify(decibels_data)
    except Exception as e:
        return jsonify({"error": str(e)})

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
            audio_data = capture_audio()
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
