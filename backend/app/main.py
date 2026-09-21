from fastapi import FastAPI
from app.database import database
from app.routers import auth, movie, theater, show, booking



app = FastAPI()

app.include_router(
    auth.router,
    prefix="/auth",
    tags =["Authentication"]
)

app.include_router(
    movie.router,
    prefix="/movies",
    tags=["Movies"]
)

app.include_router(
    theater.router,
    prefix="/theaters",
    tags=["Theaters"]
)

app.include_router(
    show.router,
    prefix="/shows",
    tags=["Shows"]
)

app.include_router(
    booking.router,
    prefix="/booking",
    tags=["Bookings"]
)


@app.on_event("startup")
async def startup():
    try:
        await database.command("ping")
        print("Connected to MongoDB")

    except Exception as e:
        print(f"MongoDB Connection Failed: {e}")


@app.get("/")
async def home():
    return {
        "message": "Movie Booking System is Running."
    }