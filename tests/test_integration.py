import unittest
import threading
import time
import requests

from client.library.server_poller import ServerPoller
from server.server import app
from common.config import Config

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

        time.sleep(2)  # Wait for the server to be up
        
    def test_client_integration(self):
        """
        Test that the client can poll the server and update statuses correctly.
        """
        base_url = Config.BASE_URL
        client = ServerPoller(base_url=base_url)
        
        for id in range(1, 3):
            # Check for pending
            print(f'Get PENDING status for ID {id}')
            client_status = client.get_status(id)
            self.assertEqual(client_status, Config.STATUS_PENDING)
            print("Sucess")
            
            print(f'Get PROCESSED status for ID {id}')
            client_status = client.get_status(id)
            server_resp = requests.get(f"{base_url}/{id}/status")
            
            status_data = server_resp.json()
            self.assertEqual(client_status, status_data.get("result", Config.STATUS_PENDING))
            
            # Check expected final status (completed or error based on id)
            if id % 2 == 0:
                self.assertEqual(client_status, Config.STATUS_COMPLETED)
            else:
                self.assertEqual(client_status, Config.STATUS_ERROR)
            print("Sucess")

        print("Test finished.")

if __name__ == '__main__':
    unittest.main()
