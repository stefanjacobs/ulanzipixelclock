
import time, random

def wait(min_seconds, max_seconds = None):
    if max_seconds is None:
        max_seconds = min_seconds
    time.sleep(random.random() * (max_seconds - min_seconds) + min_seconds)
    return
