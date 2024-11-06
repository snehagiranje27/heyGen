import requests
import polling
import logging

from common.config import Config


class ServerPoller:
    """
    A class to handle polling for status updates from a server.
    """
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        logging.info(f"ServerPoller initialized with base URL: {self.base_url}")

    def _get_status(self, id: int) -> str:
        url = f"{self.base_url}/{id}/status"        
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            status_data = resp.json()
            return status_data.get("result", Config.STATUS_PENDING)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred while getting status for ID {id}: {e}")
            raise

    def get_status(self, id: int) -> str:
        try:
            logging.info(f"Check status for ID {id}.")
            return polling.poll(
                lambda: self._get_status(id),
                step=1,
                timeout=30
            )
        except polling.TimeoutException:
            logging.warning(f"Timed out for ID {id}. Status is still pending.")
            return Config.STATUS_PENDING
        except Exception as e:
            logging.error(f"Failed to get status for ID {id}, Error: {e}")
            raise
