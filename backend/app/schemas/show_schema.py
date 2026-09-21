from pydantic import BaseModel
from datetime import datetime

class ShowCreate(BaseModel):
    movie_id: str
    theater_id: str
    show_date: str
    show_time: str
    price: float
    