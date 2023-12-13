import unittest
import requests
import threading
import time
from app import app, NoiseMeterRepository

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        # Start Flask app in a separate thread for testing
        self.server_thread = threading.Thread(target=app.run, kwargs={'host': '127.0.0.1', 'port': 5001, 'threaded': True})
        self.server_thread.start()

        # Wait for the server to start
        time.sleep(1)

    def tearDown(self):
        # Stop the Flask app after testing
        self.server_thread.join()

    def test_update_all(self):
        # Define a sample data for testing
        sample_data = [
            {"id": 1, "date": "2023-01-01", "db_volume": 50, "unit": "dB", "is_occupied": True},
            {"id": 2, "date": "2023-01-02", "db_volume": 60, "unit": "dB", "is_occupied": False}
        ]

        # Send a POST request to update the data
        response = requests.post("http://127.0.0.1:5001/update_all", json=sample_data)
        self.assertEqual(response.status_code, 200)

        # Check if the data in NoiseMeterRepository has been updated
        updated_data = NoiseMeterRepository.get_all()
        self.assertEqual(len(updated_data), 2)
        self.assertEqual(updated_data[0].DbVolume, 50)
        self.assertEqual(updated_data[1].DbVolume, 60)

    def test_is_room_occupied(self):
        # Add sample data to NoiseMeterRepository
        NoiseMeterRepository.add_noise_meter("2023-01-01", 70, "dB", True)
        NoiseMeterRepository.add_noise_meter("2023-01-02", 40, "dB", False)

        # Send a GET request to check if the room is occupied
        response = requests.get("http://127.0.0.1:5001/is_room_occupied?threshold=60")
        result = response.json()["is_room_occupied"]
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
