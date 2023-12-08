import requests

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
    decibels_data = get_decibels_data()

    if decibels_data:
        print("Received Decibel Data:")
        print(decibels_data)
