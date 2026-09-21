from fastapi import APIRouter, Depends, HTTPException
from app.schemas.show_schema import ShowCreate
from app.models.show_model import show_document
from app.database import show_collection, movie_collection, theater_collection
from app.admin import get_admin_user
from bson import ObjectId

router = APIRouter()


@router.post("/")
async def add_show(
    show: ShowCreate
):
    result = await show_collection.insert_one(
        show_document(show)
    )

    return {
        "message": "Show added successfully.",
        "id": str(result.inserted_id)
    }



@router.get("'movies/{movie_id}")
async def get_movie_shows(movie_id: str):

    shows = []

    async for show in show_collection.find(
        {"movie_id": movie_id}
    ):

        theater = await theater_collection.find_one(
            {"_id": ObjectId(show["theater_id"])}
        )

        show["_id"] = str(show["_id"])

        show["theater_name"] = (
            theater["name"] if theater else "Unkonown Theater"
        )

        shows.append(show)

    return shows


@router.get("/theater/{theater_id}")
async def get_theater_shows(theater_id: str):

    shows = []

    async for show in show_collection.find(
        {"theater_id": theater_id}
    ):
        show["_id"] = str(show["_id"])
        shows.append(show)


    return shows


@router.get("/{show_id}")
async def get_show(show_id: str):

    if not ObjectId.is_valid(show_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid show ID"
        )

    show = await show_collection.find_one(
        {"_id": ObjectId(show_id)}
    )

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )

    movie = await movie_collection.find_one(
        {"_id": ObjectId(show["movie_id"])}
    )

    theater = await theater_collection.find_one(
        {"_id": ObjectId(show["theater_id"])}
    )

    show["_id"] = str(show["_id"])

    show["movie_title"] = movie["title"] if movie else "Unknown Movie"
    show["theater_name"] = theater["name"] if theater else "Unknown Theater"

    return show    




@router.put("/{show_id}")
async def update_show(show_id: str, show: ShowCreate):

    if not ObjectId.is_valid(show_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid show ID"
        )

    result = await show_collection.update_one(
        {"_id": ObjectId(show_id)},
        {
            "$set": {
                "movie_id": show.movie_id,
                "theater_id": show.theater_id,
                "show_date": show.show_date,
                "show_time": show.show_time,
                "price": show.price
            }
        }
    )


    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )

    return {
        "message": "Show updated successfully"
    }


@router.delete("/{show_id}")
async def delete_show(show_id: str):

    if not ObjectId.is_valid(show_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid show ID"
        )


    result = await show_collection.delete_one(
        {"_id": ObjectId(show_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )

    return {
        "message": "Show deleted successfully."
    }


    