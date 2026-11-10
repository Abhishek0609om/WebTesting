import os
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

# Connect to Database EC2 IP passed via environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/crud_database")
client = AsyncIOMotorClient(MONGO_URI)
db = client.crud_database
collection = db.users

class User(BaseModel):
    name: str
    email: str
    age: int

@app.get("/api/users")
async def get_users():
    users = []
    async for user in collection.find():
        user["id"] = str(user["_id"])
        del user["_id"]
        users.append(user)
    return users

@app.post("/api/users")
async def create_user(user: User):
    result = await collection.insert_one(user.dict())
    return {"id": str(result.inserted_id), "message": "User created successfully"}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: str):
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}