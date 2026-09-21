from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.admin import get_admin_user
from app.database import theater_collection
from app.models.theater_model import theater_document
from app.schemas.theater_schema import TheaterCreate

router = APIRouter()

@router.post("/")
async def add_theater(
    theater: TheaterCreate,
    admin=Depends(get_admin_user)
):

    result = await theater_collection.insert_one(
        theater_document(theater)
    )


    return {
        "message": "Theater added successfully.",
        "id": str(result.inserted_id)
    }


@router.get("/")
async def get_all_theater():

    theaters = []

    async for theater in theater_collection.find():
        theater["_id"] = str(theater["_id"])
        theaters.append(theater)

    return theaters



@router.get("/movie/{movie_id}")
async def theaters_by_movie(movie_id: str):

    theaters = []

    async for theater in theater_collection.find(
        {"movie_id": movie_id}
    ):
        theater['_id'] = str(theater['_id'])
        theaters.append(theater)

    return theaters


@router.get("/{theater_id}")
async def get_theater(theater_id: str):
    if not ObjectId.is_valid(theater_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid theater ID"
        )

    theater = await theater_collection.find_one(
        {"_id": ObjectId(theater_id)}
    )

    if not theater:
        raise HTTPException(
            status_code=404,
            detail="Theater not found"
        )

    theater["_id"] = str(theater["_id"])

    return theater


@router.put("/{theater_id}")
async def update_theater(
    theater_id: str,
    theater: TheaterCreate,
    admin=Depends(get_admin_user)
):

    if not ObjectId.is_valid(theater_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid theater ID"
        )

    result = await theater_collection.update_one(
        {"_id": ObjectId(theater_id)},
        {
            "$set": theater_document(theater)
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Theater not found"
        )

    return {
        "message": "Theater updated successfully."
    }



@router.delete("/{theater_id}")
async def delete_theater(
    theater_id: str,
    admin=Depends(get_admin_user)
):

    if not ObjectId.is_valid(theater_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid theater ID"
        )

    result = await theater_collection.delete_one(
        {"_id": ObjectId(theater_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Theater not found"
        )

    return {
        "message": "Theater deleted successfully."
    }
    
