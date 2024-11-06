import os
from dotenv import load_dotenv


load_dotenv(os.path.join('./common/.env'))

class Config:
    # Logging configuration
    LOG_DIRECTORY = os.getenv('LOG_DIRECTORY', './logs')
    SERVER_LOG_FILE = os.getenv('SERVER_LOG_FILE', 'server.log')
    CLIENT_LOG_FILE = os.getenv('CLIENT_LOG_FILE', 'client.log')
    
    # Base URL for the server
    BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:5000')
    
    # File paths
    IDS_FILE = os.getenv('IDS_FILE', 'client/ids.json')  # Path to the IDs file
    
    # Statuses
    STATUS_NOT_PROCESSED = 'not processed'
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_ERROR = 'error'
    
    # Other common settings
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 5))  # Retry delay in seconds
    QUEUE_POLL_INTERVAL = int(os.getenv('QUEUE_POLL_INTERVAL', 1))  # Poll interval for queue
    CLIENT_POLLING_TIMEOUT = int(os.getenv('CLIENT_POLLING_TIMEOUT', 5)) # in second
    SERVER_POLLING_TIMEOUT = int(os.getenv('SERVER_POLLING_TIMEOUT', 5)) # in seconds

