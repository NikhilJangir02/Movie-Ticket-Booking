from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.mongodb_url)

database = client[settings.database_name]


user_collection = database["users"]

movie_collection = database["movies"]

theater_collection = database["theaters"]

show_collection = database["shows"]

booking_collection = database["bookings"]