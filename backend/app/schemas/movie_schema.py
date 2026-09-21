from pydantic import BaseModel
from typing import Optional

class MovieCreate(BaseModel):
    title: str
    description: str
    genre: str
    language: str
    duration: int
    release_year: int
    rating: float
    poster_url: Optional[str] = None


class MovieResponse(MovieCreate):
    id: str

