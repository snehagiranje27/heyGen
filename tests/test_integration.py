import unittest
import threading
import time
import requests
from unittest.mock import patch
from client.library.server_poller import ServerPoller
from server.server import app
from common.config import Config
import polling

def wait_for_server(base_url: str, timeout: int = 5):
    """
    Helper function to wait for the server to be up and running by checking the /ping endpoint.
    """
    for _ in range(timeout):
        try:
            response = requests.get(f"{base_url}/ping")
            if response.status_code == 200 and response.json().get("result") == "pong":
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False


class IntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up a Flask server to run in a separate thread before starting tests.
        """
        # Start Flask app in a separate thread
        cls.server_thread = threading.Thread(target=app.run, kwargs={'port': 5000, 'threaded': True, 'use_reloader': False})
        cls.server_thread.daemon = True
        cls.server_thread.start()

        # Wait for the server to be up
        if not wait_for_server(Config.BASE_URL):
            raise RuntimeError("Server not up after waiting for 5 seconds.")

    def test_integration_with_valid_id(self):
        """
        Full integration test for valid IDs, ensuring the status transitions as expected.
        """
        base_url = Config.BASE_URL
        client = ServerPoller(base_url=base_url)

        for id in range(1, 3):
            # Test for the PENDING status first
            print(f"Testing status transition for ID {id}")
            client_status = client.get_status(id=id, timeout_in_sec=5, poll=False)
            self.assertEqual(client_status, Config.STATUS_PENDING)
            print("Status is pending...")

            # Simulate status change
            time.sleep(5)

            # Test final status (Completed/Error)
            final_status = Config.STATUS_COMPLETED if id % 2 == 0 else Config.STATUS_ERROR
            client_status = client.get_status(id=id, timeout_in_sec=5, poll=True)
            self.assertEqual(client_status, final_status)
            print(f"Final status for ID {id} is {final_status} - Test passed!")

    def test_invalid_id_type(self):
        """
        Test that a ValueError is raised when a non-integer ID is provided.
        """
        base_url = Config.BASE_URL
        client = ServerPoller(base_url=base_url)

        # Test with a string ID
        with self.assertRaises(ValueError) as context:
            client.get_status(id="invalid_id", timeout_in_sec=5, poll=True)
        self.assertEqual(str(context.exception), "ID must be an integer, but got str.")

        # Test with a float ID
        with self.assertRaises(ValueError) as context:
            client.get_status(id=3.14, timeout_in_sec=5, poll=True)
        self.assertEqual(str(context.exception), "ID must be an integer, but got float.")

        # Test with None as ID
        with self.assertRaises(ValueError) as context:
            client.get_status(id=None, timeout_in_sec=5, poll=True)
        self.assertEqual(str(context.exception), "ID must be an integer, but got NoneType.")

if __name__ == '__main__':
    unittest.main()
