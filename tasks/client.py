import requests
import time

server_url = "http://192.168.50.236:8080"

def get_decibels_data():
    try:
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

if __name__ == "__main__":
    while True:
        # Fetch the average decibel levels for the last 10 minutes
        decibels_data = get_decibels_data()

        if decibels_data:
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
