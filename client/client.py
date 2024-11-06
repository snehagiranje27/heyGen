import json
import time
import logging

from queue import Queue
from common.config import Config
from client.library.server_poller import ServerPoller

class Client:
    """
    The Client class handles the logic of reading, processing, and updating IDs in the queue.
    """
    def __init__(self, filename: str, base_url: str):
        self.filename = filename
        self.id_queue = Queue()
        self.server_poller = ServerPoller(base_url=base_url)

    def load_ids_from_file(self, filename: str):
        """
        Load IDs from the json db and adding them to the queue.
        """
        try:
            with open(filename, 'r') as file:
                ids = json.load(file)
            logging.info(f"Loaded unprocessed IDs into the queue.")
            for entry in ids:
                status = entry.get('status')
                if not status or status in [Config.STATUS_PENDING, Config.STATUS_NOT_PROCESSED]:
                    self.id_queue.put(entry['id'])
        except Exception as e:
            logging.error(f"Error loading IDs from file: {e}")

    def update_id_status(self, id: int, new_status: str):
        """
        Update the status of the ID in the json db.
        """
        try:
            with open(self.filename, 'r+') as file:
                ids = json.load(file)
                for entry in ids:
                    if entry['id'] == id:
                        entry['status'] = new_status
                        break
                file.seek(0)
                json.dump(ids, file, indent=4)
                file.truncate()
            logging.info(f"Updated status of ID {id} to {new_status}.")
        except Exception as e:
            logging.error(f"Error updating ID status in file: {e}")

    def process_ids(self):
        """
        Process IDs from the queue and update their status.
        """
        while True:
            if not self.id_queue.empty():
                id = self.id_queue.get()
                logging.info(f"Processing ID {id}")
                try:
                    status = self.server_poller.get_status(id=id, timeout_in_sec=Config.CLIENT_POLLING_TIMEOUT)
                    logging.info(f"Received status for ID {id}: {status}")
                    self.update_id_status(id, status)
                except Exception as e:
                    self.update_id_status(id, Config.STATUS_NOT_PROCESSED)
                    logging.error(f"Failed to get the status of ID {id}. Added to the json db again for processing. Error: {e}")
                    
                self.id_queue.task_done()
            else:
                # If the queue is empty, do nothing (pause processing)
                time.sleep(Config.QUEUE_POLL_INTERVAL)
