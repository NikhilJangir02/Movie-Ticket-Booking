from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path(
        "<str:movie_id>/<str:theater_id>/",
        views.book_ticket,
        name="book_ticket",
    ),

    path(
        "my-booking/",
        views.my_bookings,
        name="my_booking",
    ),

    path(
        "cancel/<str:booking_id>/",
        views.cancel_booking,
        name="cancel_booking",
    ),
]
