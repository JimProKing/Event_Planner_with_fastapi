from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn
from database.connection import Database

user_router = APIRouter(
    tags=["users"]
)

user_database = Database(User)

users = {}

@user_router.post("/signup", status_code=201)
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already"
        )
    await user_database.save(user)
    return{
        "message":"user created successfully."
    }

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist"
        )
    if user_exist.password == user.password:
        return {
            "message":"user signed in successfully"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid datails passed"
    )
    # if user.email not in users:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    # if users[user.email].password != user.password:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Worng credential passed")
    # return {
    #     "message": "User signed in successfully"
    # }