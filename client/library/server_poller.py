import requests
import polling
import logging
from typing import Optional


class ServerPoller:
    """
    A class to handle polling for status updates from a server.

    This class is designed to interact with a server endpoint that provides 
    the status of a given video translation ID. It supports both one-time status checks and 
    continuous polling for updates until a specified status or timeout is reached.

    Attributes:
        base_url (str): The base URL for the server to poll. All status checks
            will use this as the root endpoint.

    Methods:
        __init__(base_url: str) -> None
            Initializes the ServerPoller with a base URL for the server.
        
        _get_status(id: int, poll: bool = True) -> str
            Sends a GET request to retrieve the status of the given ID from the 
            server. Optionally includes a `poll` parameter to control server-side 
            polling behavior.
        
        get_status(id: int, timeout_in_sec: Optional[int] = None, poll: bool = True) -> str
            Continuously polls the server for a status update of the specified ID.
            Accepts an optional timeout for the polling duration, and a poll flag 
            to enable or disable server-side polling.
    """
    
    def __init__(self, base_url: str) -> None:
        """
        Initializes the ServerPoller with a base URL.

        Args:
            base_url (str): The base URL of the server for polling status.
        
        Logs:
            Info message indicating the base URL used for polling.
        """
        self.base_url = base_url
        logging.info(f"ServerPoller initialized with base URL: {self.base_url}")

    def _get_status(self, id: int, poll: bool = True) -> str:
        """
        Fetches the current status of the specified video translation ID from the server.

        Args:
            id (int): The unique identifier for the item whose status is being retrieved.
            poll (bool, optional): If True, enables server-side polling. Defaults to True.
        
        Returns:
            str: The current status of the specified video translation ID.
        
        Raises:
            requests.exceptions.RequestException: If an error occurs while making the request.
        
        Logs:
            Error message if an error occurs during the request.
        """
        url = f"{self.base_url}/{id}/status" 
        params = {'poll': str(poll).lower()}       
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            status_data = resp.json()
            return status_data["result"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred while getting status for ID {id}: {e}")
            raise

    def get_status(self, id: int, timeout_in_sec: Optional[int] = None, poll: bool = True) -> str:
        """
        Retrieves the status of the specified video translation ID, with optional continuous polling.

        This method will either check the status once or continuously poll until
        the status changes or the timeout is reached.

        Args:
            id (int): The unique identifier for the item whose status is being retrieved.
            timeout_in_sec (Optional[int], optional): The maximum time (in seconds) to poll.
                Defaults to None (infinite timeout).
            poll (bool, optional): If True, enables server-side polling. Defaults to True.

        Returns:
            str: The final status of the specified video translation ID.

        Raises:
            polling.TimeoutException: If the polling times out before the status update.
            ValueError: If the provided `id` is not an integer.
            Exception: For any other unexpected errors.

        Logs:
            - Info message when a status check starts.
            - Warning message if polling times out.
            - Error message for any other exceptions.
        """
        if not isinstance(id, int):
            raise ValueError(f"ID must be an integer, but got {type(id).__name__}.")

        try:
            logging.info(f"Check status for ID {id}.")
            return polling.poll(
                lambda: self._get_status(id, poll),
                step=1,
                timeout=timeout_in_sec
            )
        except polling.TimeoutException:
            logging.warning(f"Timed out for ID {id}. Status is still pending.")
            raise
        except Exception as e:
            logging.error(f"Failed to get status for ID {id}, Error: {e}")
            raise
