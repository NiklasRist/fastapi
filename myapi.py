from fastapi import FastAPI, HTTPException, status, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

users = {
    1 :{
        "name":"Josh",
        "age":28,
        "role":"developer"
    }
}

# Base Pydantic Models
class User(BaseModel):
    name:str
    website:str
    age:int
    role:str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None

@app.get("/")
def root():
    return {"message":"Welcome to your Introduction to FastAPI"}

#Get User
@app.get("/users/{user_id}")
def get_user(user_id:int = Path(..., description="The ID you want to get", gt=0, lt=100)):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User Not Found!")
    return users[user_id]

# Create User
@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def create_user(user_id:int, user:User):
    if user_id in users:
        raise HTTPException(status_code=404,  detail="User already exists")
    
    users[user_id] = user.dict()
    return user
# Update User
@app.put("/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id:int, user:UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User Not Found")
    current_user = users[user_id]
    if user.name is not None:
        current_user["name"] = user.name
    if user.website is not None:
        current_user["website"] = user.website
    if user.age is not None:
        current_user["age"] = user.age
    if user.role is not None:
        current_user["role"] = user.role
    return current_user
# Delete User
@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User Not Found!")

    deleted_user = users.pop(user_id)
    return {"message":"User has been deleted", "deleted_user":deleted_user}
# Search for User
@app.get("/users/search/")
def search_by_name(name: Optional[str] = None):
    if not name:
        return {"message":"Name parameter is required"}
    
    for user in users.values():
        if user["name"] == name:
            return user
    raise HTTPException(status_code=404, detail="User not found!")