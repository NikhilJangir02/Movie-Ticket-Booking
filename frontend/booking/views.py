import requests
from django.shortcuts import render, redirect
from users.utils import get_auth_headers

FASTAPI_URL = "http://127.0.0.1:8000"

# Create your views here.
def book_ticket(request, movie_id, theater_id):

    if "token" not in request.session:
        return redirect("login")
    

    theater_response = requests.get(
        f"{FASTAPI_URL}/theaters/{theater_id}",
        headers=get_auth_headers(request)
    )

    if theater_response.status_code == 401:
        request.session.flush()
        return redirect("login")
    

    if theater_response.status_code != 200:
        return render(
            request,
            "movies/not_found.html"
        )

    theater = theater_response.json()

    if request.method == "POST":

        data = {
            "movie_id": movie_id,
            "theater_id": theater_id,
            "customer_name": request.POST.get("customer_name"),
            "email": request.POST.get("email"),
            "seats": int(request.POST.get("seats"))
        }

        response = requests.post(
            f"{FASTAPI_URL}/booking/",
            json=data,
            headers=get_auth_headers(request)
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")
        

        if response.status_code == 200:

            booking = response.json()

            return render(
                request,
                "booking/success.html",
                {
                    "booking": booking
                }
            )

        else:

            error = response.json().get("detail", "Booking failed.")

            return render(
                request,
                "booking/book_ticket.html",
                {
                    "theater": theater,
                    "error": error
                }
            )


    return render(
        request,
        "booking/book_ticket.html",
        {
            "theater": theater
        }
    )

def my_bookings(request):

    if "token" not in request.session:
        return redirect("login")

    response = requests.get(
        f"{FASTAPI_URL}/booking/",
        headers=get_auth_headers(request)
    )

    if response.status_code == 401:
        request.session.flush()
        return redirect("login")
    

    bookings = []

    if response.status_code == 200:
        bookings = response.json()

    return render(
        request,
        "booking/my_bookings.html",
        {
            "bookings": bookings
        }
    )    


def cancel_booking(request, booking_id):

    if "token" not in request.session:
        return redirect("login")

    response = requests.delete(
        f"{FASTAPI_URL}/booking/{booking_id}",
        headers=get_auth_headers(request)
    )

    print(response.status_code)
    print(response.text)

    return redirect("my_bookings")
