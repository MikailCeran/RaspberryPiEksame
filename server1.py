import numpy as np
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def calculate_decibels(audio_data):
    try:
        # Your decibel calculation logic here
        # Assuming audio_data represents the intensities of two sounds (S1 and S2)
        S1, S2 = audio_data[:len(audio_data)//2], audio_data[len(audio_data)//2:]
        
        # Calculate decibels, handle division by zero or negative values
        decibels = 10 * np.log10(np.mean(S1) / np.mean(S2))
        
        # Check for NaN or infinite values
        if np.isnan(decibels) or np.isinf(decibels):
            raise ValueError("Invalid decibel value")

        return {"decibels": decibels}
    except Exception as e:
        return {"error": str(e)}

def capture_audio():
    try:
        duration = 1  # seconds
        samplerate = 44100

        # Generate random audio data for two sounds (S1 and S2)
        S1 = 2 * np.random.random(samplerate * duration) - 1
        S2 = 2 * np.random.random(samplerate * duration) - 1

        # Concatenate S1 and S2 to represent intensities of two sounds
        audio_data = np.concatenate([S1, S2])

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
