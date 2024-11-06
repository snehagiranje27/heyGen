import logging
import os

def check_log_directory_exists(log_directory):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory, exist_ok=True)

def setup_logger(log_file_name, log_directory):
    '''
    Setup logger
    '''
    check_log_directory_exists(log_directory)
    log_path = os.path.join(log_directory, log_file_name)
    
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode='a'
    )
    logging.info(f"Logging started in {log_path}")
