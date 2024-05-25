from fastapi import FastAPI, HTTPException, APIRouter
from model.todo import to_do
from database import collection
from schema.schemas import List_serial
from bson import ObjectId  # Import ObjectId from bson
import json


# Define a router for ToDo operations
router = APIRouter()

# In-memory storage for ToDo items (This will be replaced with database operations)
to_do_items = {}


@router.get("/")
def read_root():
    cursor = collection.find({})
    todos = list(cursor)
    # Convert ObjectId to string for each document
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return todos
 

# Create a ToDo item
@router.post("/todos/", response_model=to_do)
@router.post("/todos/", response_model=to_do)
def create_todo_in_db(item: to_do):
    try:
        # Convert Pydantic model to dictionary
        todo_dict = item.dict()
        # Insert document into MongoDB collection
        result = collection.insert_one(todo_dict)
        # Check if insertion was successful
        if result.inserted_id:
            # Construct a response object with the inserted data
            response_data = {
                "_id":ObjectId(result.inserted_id),
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "complete": item.complete
            }
            return response_data
        else:
            # If insertion failed for some reason
            raise HTTPException(status_code=500, detail="Failed to create ToDo item")
    except Exception as e:
        # Handle any exceptions that occur during insertion
        raise HTTPException(status_code=500, detail=str(e))
    print(item)
    try:
        # Convert Pydantic model to dictionary
        todo_dict = item.dict()
        # Insert document into MongoDB collection
        result = collection.insert_one(todo_dict)
        # Check if insertion was successful
        if result.inserted_id:
            return {"message": "ToDo item created successfully"}
        else:
            # If insertion failed for some reason
            raise HTTPException(status_code=500, detail="Failed to create ToDo item")
    except Exception as e:
        # Handle any exceptions that occur during insertion
        raise HTTPException(status_code=500, detail=str(e))

# Retrieve a ToDo item by ID

@router.get("/todos/{item_id}", response_model=to_do)
def read_to_do(item_id: str):
    try:
        # Convert item_id to ObjectId
        object_id = ObjectId(item_id)
        # Retrieve the ToDo item from the database
        todo_item = collection.find_one({"_id": object_id})
        # Check if item exists
        if todo_item:
            return todo_item
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update a ToDo item by ID
@router.put("/todos/{item_id}")
def update_todo_in_db(item_id: str, new_item: dict):
    # Update document in MongoDB collection
    result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": new_item})
    
    if result.modified_count > 0:
        return {"message": "ToDo item updated successfully"}
    elif result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    else:
        return {"message": "No changes detected"}
    
    
# Delete a ToDo item by ID

@router.delete("/todos/{item_id}")
def delete_to_do(item_id: str):
    try:
        # Delete the ToDo item from the database
        result = collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 1:
            return {"message": "ToDo item deleted successfully"}
        else:
            # If no item was deleted, raise an HTTPException with 404 status code
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        # Handle any exceptions that occur during the operation
        raise HTTPException(status_code=500, detail=str(e))
