from fastapi import APIRouter, HTTPException
from app.schemas.user_schemas import UserRegister, UserUpdate
from app.models.user_model import user_document
from app.database import user_collection
from app.security import hash_password
from app.schemas.user_schemas import UserLogin
from app.security import verify_password, create_access_token
from fastapi import Depends
from app.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schemas import ChangePassword


router = APIRouter()


@router.post("/register")
async def register(user: UserRegister):

    existing_user = await user_collection.find_one({"email": user.email})


    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    #Hash the password
    user.password = hash_password(user.password)

    #Convert schema to MongoDB document
    new_user = user_document(user)

    #Insert into MongoDB
    await user_collection.insert_one(new_user)

    return {
        "message": "User registered successfully."
    }


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    existing_user = await user_collection.find_one(
        {"email": form_data.username}
    )

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if not verify_password(
        form_data.password,
        existing_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token(
        {
            "sub": str(existing_user["_id"]),
            "email": existing_user["email"],
            "role": existing_user["role"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/profile")
async def profile(
    current_user=Depends(get_current_user)
):

    return {
        "id": current_user["_id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

@router.put("/profile")
async def update_profile(
    user: UserUpdate,
    current_user=Depends(get_current_user)
):

    await user_collection.update_one(
        {
            "_id": current_user["_id"]
        },
        {
            "$set":{
                "name": user.name,
                "email": user.email
            }
        }
    )

    return {
        "message": "Profile updated successfully."
    }

@router.put("/change_password")
async def change_password(
    password: ChangePassword,
    current_user=Depends(get_current_user)
):

    if not verify_password(
        password.current_password,
        current_user["password"]
    ):

        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect."
        )

    hashed_password= hash_password(
        password.new_password
    )

    await user_collection.update_one(
        {"_id": current_user["_id"]},
        {
            "$set":{
                "password": hashed_password
            }
        }
    )

    return {
        "message": "Password changed successfully."
    }