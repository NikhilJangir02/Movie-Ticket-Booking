from pydantic import BaseModel, EmailStr


class BookingCreate(BaseModel):
    movie_id: str
    theater_id: str
    customer_name: str
    email: EmailStr
    seats: int
    