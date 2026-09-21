from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.dependencies import get_current_user
from app.database import booking_collection, theater_collection, movie_collection
from app.models.booking_model import booking_document
from app.schemas.booking_schema import BookingCreate

router = APIRouter()

@router.post("/")
async def create_booking(
    booking: BookingCreate,
    current_user=Depends(get_current_user)
    ):

    theater = await theater_collection.find_one(
        { "_id": ObjectId(booking.theater_id)}
    )


    if not theater:
        raise HTTPException(
            status_code=404,
            detail="Theater not found"
        )

    if booking.seats <= 0:
        raise HTTPException(
            status_code=400,
            detail="Seats must be greater than zero."
        )

    if booking.seats > theater["total_seats"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough seats available."
        )

    booking_data = booking_document(booking)

    booking_data["user_id"] = str(current_user["_id"])

    result = await booking_collection.insert_one(
        booking_data
    )


    await theater_collection.update_one(
        {"_id": ObjectId(booking.theater_id)},
        {
            "$inc": {
                "total_seats": -booking.seats
            }
        }
    )


    return {
        "message": "Booking successful",
        "booking_id": str(result.inserted_id)
    }


@router.get("/")
async def get_all_bookings(
    current_user=Depends(get_current_user)
):

    bookings = []

    # Admin can see all bookings
    if current_user["role"] == "admin":
        cursor = booking_collection.find()
    else:
        # Users can only see their own bookings
        cursor = booking_collection.find(
            {
                "user_id": str(current_user["_id"])
            }
        )

    async for booking in cursor:

        booking["_id"] = str(booking["_id"])
        booking["id"] = booking["_id"]

        # Movie Details
        movie = None
        if ObjectId.is_valid(booking["movie_id"]):
            movie = await movie_collection.find_one(
                {"_id": ObjectId(booking["movie_id"])}
            )

        # Theater Details
        theater = None
        if ObjectId.is_valid(booking["theater_id"]):
            theater = await theater_collection.find_one(
                {"_id": ObjectId(booking["theater_id"])}
            )

        booking["movie_name"] = (
            movie["title"] if movie else "Unknown Movie"
        )

        booking["theater_name"] = (
            theater["name"] if theater else "Unknown Theater"
        )

        bookings.append(booking)

    return bookings    


@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: str,
    current_user=Depends(get_current_user)
):

    print("Booking ID:", booking_id)
    print("Current User:", current_user)

    if not ObjectId.is_valid(booking_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid booking ID"
        )

    booking = await booking_collection.find_one(
        {"_id": ObjectId(booking_id)}
    )

    print("Booking Found:", booking)

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if (
        current_user["role"] != "admin"
        and booking["user_id"] != str(current_user["_id"])
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to cancel this booking."
        )

    result = await booking_collection.delete_one(
        {"_id": ObjectId(booking_id)}
    )

    print("Deleted Count:", result.deleted_count)

    return {
        "message": "Booking cancelled successfully."
    }