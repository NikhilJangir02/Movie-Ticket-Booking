from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends

from app.admin import get_admin_user
from app.database import movie_collection
from app.models.movie_model import movie_document
from app.schemas.movie_schema import MovieCreate

router = APIRouter()

@router.post("/")
async def add_movie(movie: MovieCreate):

    new_movie = movie_document(movie)

    result = await movie_collection.insert_one(new_movie)

    return {
        "message": "Movie added successfully.",
        "id": str(result.inserted_id)
    }


@router.get("/")
async def get_all_movies():

    movies = []

    async for movie in movie_collection.find():
        movie["_id"] = str(movie["_id"])
        movies.append(movie)

    return movies


@router.get("/{movie_id}")
async def get_movie(movie_id: str):

    if not ObjectId.is_valid(movie_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid movie ID"
        )

    movie = await movie_collection.find_one(
        {"_id": ObjectId(movie_id)}
    )

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    movie["_id"] = str(movie["_id"])

    return movie


@router.put("/{movie_id}")
async def update_movie(
    movie_id: str,
    movie: MovieCreate,
    admin= Depends(get_admin_user)
):

    if not ObjectId.is_valid(movie_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid moive ID"
        )

    result = await movie_collection.update_one(
        {"_id": ObjectId(movie_id)},
        {
            "$set": {
                "title": movie.title,
                "description": movie.description,
                "genre": movie.genre,
                "language": movie.language,
                "duration": movie.duration,
                "release_year": movie.release_year,
                "rating": movie.rating,
                "poster_url": movie.poster_url
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return {
        "message": "Movie updated successfully"
    }


@router.delete("/{movie_id}")
async def delete_movie(
    movie_id: str
):
    if not ObjectId.is_valid(movie_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid movie ID"
        )

    result = await movie_collection.delete_one(
        {"_id": ObjectId(movie_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return {
        "message":"Movie deleted successfully."
    }