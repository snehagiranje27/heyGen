# HeyGen Challenge

This is a simple client-server system where the client polls the server (using flask) for the status of IDs and updates a local JSON file based on the responses. The server simulates the status changes and responds accordingly.

## Project Structure

```bash
.
├── client                 # Contains the client-side logic
├── common                 # Common configuration and logger setup
├── logs                   # Directory for log files
├── server                 # Contains the server-side logic
├── tests                  # Integration tests
├── requirements           # Requirement file
```



## Getting Started

### Prerequisites
- Python 3.9+

### Install required dependencies by running:

1. Clone the repository:
   ```bash
   git clone https://github.com/snehagiranje27/heyGen.git
   ```

2. Navigate to the project directory:
   ```bash
   cd heyGen
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

5. Install the required dependencies using the requirements.txt file located in the requirements directory:
    ```bash
    pip install -r requirements/requirements.txt
    ```

### Running the Server and Client

1. In one terminal, run the server:
   ```bash
   cd heyGen
   source venv/bin/activate
   python -m server.server
   ```

2. In another terminal, run the client:
   ```bash
   cd heyGen
   source venv/bin/activate
   python -m client.main
   ```

    The client is fully automated. You can add IDs to process in the ids.json file in the following format, and it will process them and update the JSON file with the latest status:
    ```json
    {
        "id": 5
    }
    ```
    It's always better to use a database, but for simplicity, JSON is used here.

### Logs
You can also view the server and client logs in the logs directory.

### Integration Tests
To ensure everything is working correctly, you can run the integration tests:
```bash
cd heyGen
python -m unittest tests/test_integration.py
```