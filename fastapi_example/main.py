from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict
import time
import uvicorn
import sys
import json
import os
import asyncio

app = FastAPI()

# Data file path
DATA_FILE = "data.json"

# In-memory data store (replace with a database in a real application)
items = {}
item_id_counter = 0

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# Middleware to log request duration
@app.middleware("http")
async def log_request_duration(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request {request.method} {request.url} took {process_time:.3f}s")
    return response

# Create item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    global item_id_counter
    item_id_counter += 1
    item_id = item_id_counter
    items[item_id] = item
    save_data()
    return item

# Read item
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# Update item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    save_data()
    return item

# Delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    save_data()
    return {"message": "Item deleted"}

# Get all item IDs
@app.get("/items/", response_model=Dict[int, Item])
async def read_all_items():
    return items

# Get all item IDs
@app.get("/item_ids/", response_model=List[int])
async def get_all_item_ids():
    return list(items.keys())

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

def save_data():
    data = {"items": {k: v.dict() for k, v in items.items()}, "item_id_counter": item_id_counter}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    global items, item_id_counter
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        items = {int(k): Item(**v) for k, v in data["items"].items()}
        item_id_counter = data["item_id_counter"]

def start_server():
    load_data()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

async def test_saving_and_loading():
    global items, item_id_counter

    # Create some sample items
    item1 = Item(name="Item 1", description="Description 1", price=10.0, tax=1.0)
    item2 = Item(name="Item 2", description="Description 2", price=20.0, tax=2.0)
    item_id_counter = 0
    items = {}
    await create_item(item1)
    await create_item(item2)

    # Save the data
    save_data()

    # Clear the in-memory data
    items = {}
    item_id_counter = 0

    # Load the data
    load_data()

    # Verify that the loaded data is correct
    if 1 not in items or 2 not in items:
        print("Error: Item IDs not loaded correctly.")
        return

    loaded_item1 = items[1]
    loaded_item2 = items[2]

    if loaded_item1.name != item1.name or loaded_item1.description != item1.description or loaded_item1.price != item1.price or loaded_item1.tax != item1.tax:
        print("Error: Item 1 not loaded correctly.")
        return

    if loaded_item2.name != item2.name or loaded_item2.description != item2.description or loaded_item2.price != item2.price or loaded_item2.tax != item2.tax:
        print("Error: Item 2 not loaded correctly.")
        return

    print("Saving and loading test passed!")


if __name__ == "__main__":
    asyncio.run(test_saving_and_loading())
