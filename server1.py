import numpy
import sounddevice as sd
from flask import Flask, jsonify

app = Flask(__name__)

def capture_decibels():
    duration = 1  # seconds
    samplerate = 44100

    # Capture audio
    audio_data, _ = sd.read(samplerate=samplerate, channels=1, dtype='int16', duration=duration)

    # Calculate decibel level using numpy
    rms = numpy.sqrt(numpy.mean(audio_data**2))
    decibel_data = 20 * numpy.log10(rms)

    return decibel_data

@app.route('/get_decibels', methods=['GET'])
def get_decibels():
    try:
        decibel_data = capture_decibels()
        return jsonify({"decibel_data": decibel_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
