import sounddevice as sd
import numpy as np
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def capture_decibels():
    duration = 1  # seconds
    samplerate = 44100

    # Capture audio
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    # Calculate decibel level
    rms = np.sqrt(np.mean(np.square(audio_data)))
    decibel_data = 20 * np.log10(rms)

    return decibel_data

@app.route('/get_decibels', methods=['GET'])
def get_decibels():
    decibel_data = capture_decibels()
    return jsonify({"decibel_data": decibel_data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
