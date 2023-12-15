import requests
import time
import numpy as np  # Ensure numpy is imported for processing audio data

# Update the server_url to the local Flask server on Raspberry Pi
local_server_url = "http://192.168.156.236:8080"

# Update the server_url_azure to the Azure API endpoint
azure_server_url = "https://noisemeterapi.azurewebsites.net"

def capture_audio():
    # Simulate capturing audio by generating random decibel values
    return np.random.uniform(low=30, high=80, size=44100)  # Random values between 30 and 80

def send_audio_data(audio_data, server_url):
    try:
        response = requests.post(f"{server_url}/upload_audio", json={"audio_data": audio_data.tolist()})
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_decibels_data(server_url):
    try:
        audio_data = capture_audio()

        # Optionally, process audio_data if needed

        # Send audio data to the server (local or Azure) based on the server_url
        send_audio_data(audio_data, server_url)

        # Fetch other data from the server (local or Azure) based on the server_url
        response = requests.get(f"{server_url}/get_decibels_data")
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    while True:
        # Fetch the average decibel levels for the last 10 minutes from the local server
        decibels_data_local = get_decibels_data(local_server_url)

        if decibels_data_local and decibels_data_local["average_pr_1min"]:
            # Display the average decibel levels for the last 10 minutes
            print("Average Decibel Readings for the Last 10 Minutes (Local Server):")
            for average, timestamp in decibels_data_local["average_pr_10min"]:
                print(f"{timestamp}: {average} dB")

            # Display the current average decibel level
            current_average = decibels_data_local["average_pr_1min"][-1][0]
            current_timestamp = decibels_data_local["average_pr_1min"][-1][1]
            print(f"\nCurrent Average Decibel Reading ({current_timestamp}): {current_average} dB")

        # Send audio data to the Azure API
        send_audio_data(capture_audio(), azure_server_url)

        # Fetch the average decibel levels for the last 10 minutes from the Azure API
        decibels_data_azure = get_decibels_data(azure_server_url)

        if decibels_data_azure and decibels_data_azure["average_pr_1min"]:
            # Display the average decibel levels for the last 10 minutes
            print("\nAverage Decibel Readings for the Last 10 Minutes (Azure API):")
            for average, timestamp in decibels_data_azure["average_pr_10min"]:
                print(f"{timestamp}: {average} dB")

            # Display the current average decibel level
            current_average_azure = decibels_data_azure["average_pr_1min"][-1][0]
            current_timestamp_azure = decibels_data_azure["average_pr_1min"][-1][1]
            print(f"\nCurrent Average Decibel Reading ({current_timestamp_azure}): {current_average_azure} dB")

        # Wait for 1 minute before fetching data again
        time.sleep(60)
