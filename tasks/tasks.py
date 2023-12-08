# tasks/tasks.py
from celery import Celery
from server1 import capture_audio
import numpy as np

celery = Celery('tasks', broker='pyamqp://guest:guest@localhost//')

@celery.task
def calculate_and_send_decibels(audio_data):
    try:
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
