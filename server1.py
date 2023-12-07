import soundfile as sf
import sounddevice as sd
from flask import Flask, jsonify
from flask_cors import CORS  # Import the CORS extension

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def capture_audio():
    duration = 1  # seconds
    samplerate = 44100
    filename = 'captured_audio.wav'

    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    sf.write(filename, audio_data, samplerate)
    print(f"Audio captured and saved to {filename}")
    return filename

@app.route('/get_audio', methods=['GET'])
def get_audio():
    filename = capture_audio()
    return jsonify({"audio_file": filename})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
