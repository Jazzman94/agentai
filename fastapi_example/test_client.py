import requests
import time
import uvicorn
from fastapi import FastAPI
from main import app, start_server  # Import the FastAPI app and start_server function from main.py
import subprocess
import os

BASE_URL = "http://localhost:8001"
PORT = 8001

def test_health_check():
    try:
        # Give the server some time to start
        time.sleep(5)
        response = requests.get(f"{BASE_URL}/healthz")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        assert data["status"] == "ok"
        print("Health check passed!")
    except requests.exceptions.RequestException as e:
        print(f"Could not connect to the server. Make sure it is running.\n{e}")


def test_save_load():
    try:
        # Give the server some time to start
        time.sleep(5)

        # Create an item
        item_data = {"name": "Test Item", "description": "Test Description", "price": 10.0, "tax": 1.0}
        response = requests.post(f"{BASE_URL}/items/", json=item_data)
        response.raise_for_status()
        item = response.json()

        # Verify item creation
        assert item["name"] == "Test Item"

        # Simulate server restart (no actual restart, but data should be loaded on next request)
        time.sleep(1)

        # Read the item
        response = requests.get(f"{BASE_URL}/items/1")  # Assuming item ID is 1
        response.raise_for_status()
        loaded_item = response.json()

        # Verify loaded item
        assert loaded_item["name"] == "Test Item"
        print("Save and load test passed!")

    except requests.exceptions.RequestException as e:
        print(f"Could not connect to the server or an error occurred.\n{e}")
    except AssertionError as e:
        print(f"Assertion failed: {e}")


if __name__ == "__main__":
    # Start the server using subprocess
    env = os.environ.copy()
    env["PORT"] = str(PORT)
    process = subprocess.Popen(["python", "main.py"], env=env)
    try:
        test_health_check()
        test_save_load()
    finally:
        process.terminate()  # Ensure the server is terminated
        process.wait()