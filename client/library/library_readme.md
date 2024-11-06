# ServerPoller Library

The `ServerPoller` is Python library that provides functionality for checking and polling the status of items on a server. It uses HTTP requests to interact with a server endpoint and supports both one-time status checks and continuous polling with a configurable timeout.

## Features

- **Base URL Initialization**: Initialize with a server base URL.
- **Single Status Check**: Retrieve the status of an item by its ID.
- **Continuous Polling**: Poll the server at specified intervals until a status update or timeout.
- **Timeout Handling**: Configurable timeout for polling operations.
- **Error Handling**: Graceful handling of request errors, with detailed logging.

## Installation

- `requests`: For making HTTP requests
- `polling`: For continuous polling with customizable intervals

To install these dependencies, run:

```bash
pip install requests polling
```

## Usage

### Initialization

Create an instance of `ServerPoller` by providing the base URL of your server:

```python
from server_poller import ServerPoller

base_url = "http://127.0.0.1:5000" # Your server detail
poller = ServerPoller(base_url)
```

### Single Status Check

To check the status of an item by its ID without continuous polling:

```python
status = poller._get_status(id=1, poll=False)
print(f"Status: {status}")
```

### Continuous Polling with Timeout

To continuously poll for a status update until a specified timeout:

```python
try:
    status = poller.get_status(id=1, timeout_in_sec=10, poll=True)
    print(f"Status: {status}")
except polling.TimeoutException:
    print("Polling timed out. Status is still pending.")
except Exception as e:
    print(f"An error occurred: {e}")
```

### Parameters

- **`id` (int)**: The unique identifier for the item whose status is being checked.
- **`poll` (bool)**: When set to `True`, enables server-side polling if supported.
- **`timeout_in_sec` (Optional[int])**: Maximum time (in seconds) to wait for the status.

### Logging

The library provides informative logging messages:

- **Info**: Indicates the start of a status check.
- **Warning**: Warns if polling times out.
- **Error**: Logs any request errors encountered.

### Example

```python
poller = ServerPoller("http://localhost:5000")

try:
    status = poller.get_status(id=42, timeout_in_sec=2, poll=True)
    print("Status:", status)
except polling.TimeoutException:
    print("Timed out waiting for status.")
except Exception as e:
    print("An error occurred:", str(e))
```
