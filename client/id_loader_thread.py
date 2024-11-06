import time
import logging
import threading

from common.config import Config


class IDLoaderThread(threading.Thread):
    """
    Thread that continuously loads new IDs from the JSON file and adds them to the queue.
    """
    def __init__(self, client, filename: str):
        super().__init__()
        self.client = client
        self.filename = filename

    def run(self):
        while True:
            try:
                self.client.load_ids_from_file(self.filename)
                time.sleep(Config.RETRY_DELAY)  # Wait for a while before reloading IDs
            except Exception as e:
                logging.error(f"Error loading IDs: {e}")
                time.sleep(Config.RETRY_DELAY)
