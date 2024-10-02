from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from io import BytesIO
import db
import pymongo
from typing import Dict, Any
import re
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["mydatabase"]
mycol = mydb["users"]

dblist = client.list_database_names()
if "mydatabase" in dblist:
    print("The database exists.")
else:
    print("DB doesnt exist")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the frontend domain like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    is_locked: bool
    usertype: str
    

def is_valid_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.get("/")
def getRoot():
    return{1:"heyheyhey"}

@app.get("/users")
def getAllUsers():
    return mycol.find()

@app.get("/users/{username}")
def getUserByUsername(username):
    query = {"username": username}
    result = mycol.find(query)
    if not result:
        raise HTTPException(status_code=404, detail="User does not exist")
    return {"username": username}

@app.post("/register")
def registerUser(user: User):
    uniqueUserCheck = mycol.find_one({"username": user.username})
    if uniqueUserCheck:
        raise HTTPException(status=409, detail="User already exists")
        
    result = mycol.insert_one({
            "username": user.username,
            "email": user.email,
            "usertype": user.usertype
        })
    if result.inserted_id:
        return{"message": "Registered successfully"}
    else:
        raise HTTPException(status_code=500, detail="Insert failed")

@app.delete("/delete")
def deleteUserByID(user: User):
    if mycol.find({"username":user.username}).count()==0:
        raise HTTPException(status_code=404, detail="User not found")
    result = mycol.delete_one({"username": user.username})
    
    