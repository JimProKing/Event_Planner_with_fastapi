from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

user_router = APIRouter(
    tags=["users"]
)
users = {}

@user_router.post("/signup", status_code=201)
async def sign_new_user(data: User) -> dict:
    if data.email in users:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    users[data.email] = data
    return {
        "message": "User created successfully",
        "user": data
    }

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    if user.email not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    if users[user.email].password != user.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Worng credential passed")
    return {
        "message": "User signed in successfully"
    }