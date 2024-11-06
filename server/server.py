import polling
import logging

from flask import Flask, request

from server.db import InMemoryDB
from common.logger_setup import setup_logger
from common.config import Config


setup_logger(Config.SERVER_LOG_FILE, Config.LOG_DIRECTORY)

app = Flask(__name__)

db = InMemoryDB()

def get_terminating_status_or_none(id):
    status = db.get_status(id)
    if status != Config.STATUS_PENDING:
        return {"result" : status}
    return None

@app.route('/ping', methods=['GET'])
def ping():
    """
    Simple ping endpoint that returns pong, just to check if server is up or not.
    """
    return {"result": "pong"}, 200

@app.route('/<int:id>/status', methods=['GET'])
def get_status(id: int):
    poll = request.args.get('poll', 'false').lower() == 'true'
    if not poll:
        try:
            status = db.get_status(id)
            logging.info(f"Retrieved current status for ID {id}: {status}")
            return {"result": status}
        except Exception as e:
            logging.error(f"Failed to get status for ID {id}, Error: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500
    try:
        logging.info(f"Status check request for ID {id}")
        return polling.poll(
            lambda: get_terminating_status_or_none(id),
            step=1,
            timeout=Config.SERVER_POLLING_TIMEOUT
        )
    except polling.TimeoutException:
        logging.warning(f"Timed out for ID {id}. Status is still pending.")
        return {"result" : Config.STATUS_PENDING }
    except Exception as e:
        logging.error(f"Failed to get status for ID {id}, Error: {str(e)}")
        return {"error": "An unexpected error occurred"}, 500


if __name__ == '__main__':
    logging.info("Server is starting...")
    app.run()
