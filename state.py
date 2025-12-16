from collections import deque
import threading

class GlobalState:
    def __init__(self, max_ticks=50000):
        self.lock = threading.Lock()
        self.ticks = deque(maxlen=max_ticks)
        self.bars = {
            "1s": {},
            "1m": {},
            "5m": {}
        }

STATE = GlobalState()
