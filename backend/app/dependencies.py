from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.database import user_collection
from app.security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

async def get_current_user(
        token: str = Depends(oauth2_scheme)
):
    payload = verify_access_token(token)

    user = await user_collection.find_one(
        {
            "email": payload["email"]
        }
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    user["_id"] = str(user["_id"])

    return user