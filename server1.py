import numpy as np
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def calculate_decibels(audio_data):
    try:
        # Your decibel calculation logic here
        # This example assumes the audio data is in the range [-1, 1]
        decibels = 20 * np.log10(np.max(np.abs(audio_data)))
        return decibels
    except Exception as e:
        return {"error": str(e)}

def capture_audio():
    try:
        duration = 1  # seconds
        samplerate = 44100

        # Generate random audio data in the range [-1, 1]
        audio_data = 2 * np.random.random(samplerate * duration) - 1

        return audio_data
    except Exception as e:
        return {"error": str(e)}

@app.route('/get_decibels', methods=['GET'])
def get_decibels():
    try:
        audio_data = capture_audio()
        decibels = calculate_decibels(audio_data)
        return jsonify({"decibels": decibels})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
