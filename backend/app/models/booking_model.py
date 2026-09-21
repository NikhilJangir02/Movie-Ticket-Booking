from datetime import datetime, timezone

def booking_document(booking):
    return {
        "movie_id": booking.movie_id,
        "theater_id": booking.theater_id,
        "customer_name": booking.customer_name,
        "email": booking.email,
        "seats": booking.seats,
        "booking_time": datetime.now(timezone.utc)
    }