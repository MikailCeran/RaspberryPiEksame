import requests
import time
import numpy as np  # Ensure numpy is imported for processing audio data

# Update the server_url to the local Flask server
server_url = "http://192.168.50.236:8080"


def capture_audio():
    # Simulate capturing audio by generating random decibel values
    return np.random.uniform(low=30, high=80, size=44100)  # Random values between 30 and 80

def send_audio_data(audio_data):
    try:
        response = requests.post(f"{server_url}/upload_audio", json={"audio_data": audio_data.tolist()})
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_decibels_data():
    try:
        audio_data = capture_audio()

        # Optionally, process audio_data if needed

        # Send audio data to the local Flask server
        send_audio_data(audio_data)

        # Fetch other data from the local Flask server (if needed)
        response = requests.get(f"{server_url}/get_decibels_data")
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    while True:
        # Fetch the average decibel levels for the last 10 minutes
        decibels_data = get_decibels_data()

        if decibels_data and decibels_data["average_pr_1min"]:
            # Display the average decibel levels for the last 10 minutes
            print("Average Decibel Readings for the Last 10 Minutes:")
            for average, timestamp in decibels_data["average_pr_10min"]:
                print(f"{timestamp}: {average} dB")

            # Display the current average decibel level
            current_average = decibels_data["average_pr_1min"][-1][0]
            current_timestamp = decibels_data["average_pr_1min"][-1][1]
            print(f"\nCurrent Average Decibel Reading ({current_timestamp}): {current_average} dB")

        # Wait for 1 minute before fetching data again
        time.sleep(60)
