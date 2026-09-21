from pydantic import BaseModel

class TheaterCreate(BaseModel):
    name: str
    city: str
    address: str
    total_seats: int
    movie_id: str


class TheaterResponse(TheaterCreate):
    id: str    