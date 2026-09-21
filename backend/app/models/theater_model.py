from datetime import datetime, timezone

def theater_document(theater):

    return {
        "name": theater.name,
        "city": theater.city,
        "address": theater.address,
        "total_seats": theater.total_seats,
        "movie_id": theater.movie_id,
        "created_at": datetime.now(timezone.utc)
    }