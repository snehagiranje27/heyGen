import logging

from client.client import Client
from client.id_loader_thread import IDLoaderThread
from common.logger_setup import setup_logger
from common.config import Config

# Setup logger
setup_logger(Config.CLIENT_LOG_FILE, Config.LOG_DIRECTORY)

if __name__ == '__main__':
    logging.info("Client is starting...")
    client = Client(filename=Config.IDS_FILE, base_url=Config.BASE_URL)

    loader_thread = IDLoaderThread(client=client, filename=Config.IDS_FILE)
    loader_thread.daemon = True 
    loader_thread.start()

    client.process_ids()
