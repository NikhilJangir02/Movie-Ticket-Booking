from datetime import datetime, timezone

def show_document(show):
    return {
        "movie_id": show.movie_id,
        "theater_id": show.theater_id,
        "show_time": show.show_time,
        "price": show.price,
        "created_at": datetime.now(timezone.utc)
    }