import random

class Repo():
    def get_random_volume_db(self):
        # Generate a random integer between 1 and 40
        volume_db = random.randint(1, 40)
        return volume_db

# Example usage:
repo_instance = Repo()
random_volume = repo_instance.get_random_volume_db()
print("Random VolumeDB:", random_volume)
