import numpy
import sounddevice as sd
from flask import Flask, jsonify
import time

app = Flask(__name__)

def capture_decibels():
    duration = 1
    samplerate = 44100

    # Capture audio
    audio_data, _ = sd.read(samplerate=samplerate, channels=1, dtype='int16', duration=duration)

    # Calculate decibels
    rms = numpy.sqrt(numpy.mean(audio_data**2))
    decibel_data = 20 * numpy.log10(rms)

    return decibel_data

@app.route('/get_decibels', methods=['GET'])
def get_decibels():
    decibel_data = capture_decibels()
    return jsonify({"decibel_data": decibel_data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
