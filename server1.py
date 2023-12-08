# server1.py
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from tasks.tasks import calculate_and_send_decibels  # Adjust the import statement
from apscheduler.schedulers.background import BackgroundScheduler
import numpy as np
import scipy.io.wavfile as wav
import json

app = Flask(__name__)
CORS(app)

# Initialize variables to store decibels data
decibels_data = {"current": [], "average_pr_10min": []}
decibels_window = []

# Schedule the task to run every minute
scheduler = BackgroundScheduler()

def save_decibels_to_json():
    global decibels_window

    # Calculate the average decibels over the past 10 minutes
    if len(decibels_window) == 10:
        average_pr_10min = np.mean(decibels_window)
        decibels_data["average_pr_10min"].append(average_pr_10min)
        decibels_window = []  # Reset the window after calculating the average
    else:
        average_pr_10min = None

    # Save the current decibels to the data
    current_decibels = calculate_and_send_decibels(capture_audio())["decibels"]
    decibels_data["current"].append(current_decibels)

    # Save the data to a JSON file
    with open('decibels_data.json', 'w') as json_file:
        json.dump(decibels_data, json_file)

# Schedule the task to run every minute
scheduler.add_job(save_decibels_to_json, 'interval', minutes=1)
scheduler.start()

def capture_audio():
    try:
        duration = 1  # seconds
        samplerate = 44100

        # Generate random audio data for two sounds (S1 and S2)
        S1 = 2 * np.random.random(samplerate * duration) - 1
        S2 = 2 * np.random.random(samplerate * duration) - 1

        # Concatenate S1 and S2 to represent intensities of two sounds
        audio_data = np.concatenate([S1, S2])

        # Save the audio data to a WAV file
        wav.write('captured_audio.wav', samplerate, audio_data.astype(np.int16))

        return audio_data
    except Exception as e:
        return {"error": str(e)}

@app.route('/get_decibels', methods=['GET'])
def get_decibels():
    try:
        audio_data = capture_audio()
        decibels = calculate_and_send_decibels(audio_data)
        return jsonify({"decibels": decibels["decibels"]})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/captured_audio', methods=['GET'])
def get_captured_audio():
    try:
        return send_file('captured_audio.wav', as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
