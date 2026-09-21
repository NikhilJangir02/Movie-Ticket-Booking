from fastapi import Depends, HTTPException

from app.dependencies import get_current_user


async def get_admin_user(
        current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can perform this action."
        )
    return current_user