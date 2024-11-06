import time
from common.config import Config


class InMemoryDB:
    """
    A simple in-memory database to manage the status of requests.
    """

    def __init__(self):
        self.db = {}

    def get_status(self, id: int) -> str:
        if id not in self.db.keys():
            self.db[id] = time.time()
        return self._get_status(id)
        
    def _get_status(self, id: int) -> str:
        curr_time = time.time()
        return Config.STATUS_PENDING if curr_time - self.db[id] < 10 else (Config.STATUS_COMPLETED if id % 2 == 0 else Config.STATUS_ERROR)
