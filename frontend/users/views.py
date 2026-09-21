import requests
from django.shortcuts import render, redirect
from users.utils import get_auth_headers

# Create your views here.
FASTAPI_URL = "http://127.0.0.1:8000"

def register_view(request):

    if request.session.get("token"):
        return redirect("home")

    if request.method == "POST":

        data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password")
        }

        response = requests.post(
            f"{FASTAPI_URL}/auth/register",
            json=data
        )

        if response.status_code == 200:

            return redirect("login")

        error = response.json().get(
            "detail",
            "Registration failed."
        )

        return render(
            request,
            "users/register.html",
            {
                "error": error
            }
        )

    return render(
        request,
        "users/register.html"
    )




def login_view(request):

    if request.session.get("token"):
        return redirect("home")

    if request.method == "POST":

        data = {
            "username": request.POST.get("email"),
            "password": request.POST.get("password")
        }

        response = requests.post(
            f"{FASTAPI_URL}/auth/login",
            data=data
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        if response.status_code == 200:

            result = response.json()

            request.session["token"] = result["access_token"]

            # Get logged-in user profile
            profile_response = requests.get(
                f"{FASTAPI_URL}/auth/profile",
                headers={
                    "Authorization": f"Bearer {result['access_token']}"
                }
            )

            if profile_response.status_code == 200:
                profile = profile_response.json()

                request.session["role"] = profile["role"]
                request.session["name"] = profile["name"]
                request.session["email"] = profile["email"]

            return redirect("home")

        return render(
            request,
            "users/login.html",
            {
                "error": response.json().get(
                    "detail",
                    "Invalid email or password"
                )
            }
        )

    return render(
        request,
        "users/login.html"
    )

def logout_view(request):
    request.session.flush()
    return redirect("login")


def profile(request):

    if "token" not in request.session:
        return redirect("login")

    response = requests.get(
        f"{FASTAPI_URL}/auth/profile",
        headers=get_auth_headers(request)
    )

    if response.status_code == 401:
        request.session.flush()
        return redirect("login")

    user = response.json()

    return render(
        request,
        "users/profile.html",
        {
            "user": user
        }
    )

def edit_profile(request):

    if "token" not in request.session:
        return redirect("login")

    profile_response = requests.get(
        f"{FASTAPI_URL}/auth/profile",
        headers=get_auth_headers(request)
    )

    if profile_response.status_code == 401:
        request.session.flush()
        return redirect("login")

    user = profile_response.json()

    if request.method == "POST":

        data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email")
        }

        response = requests.put(
            f"{FASTAPI_URL}/auth/profile",
            json=data,
            headers=get_auth_headers(request)
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")

        if response.status_code == 200:
            return redirect("profile")

        return render(
            request,
            "users/edit_profile.html",
            {
                "user": user,
                "error": response.json()
            }
        )


    return render(
        request,
        "users/edit_profile.html",
        {
            "user": user
        }
    )

def change_password(request):

    if "token" not in  request.session:
        return redirect("login")

    if request.method == "POST":

        data = {

            "current_password": request.POST.get("current_password"),
            "new_password": request.POST.get("new_password")
        }

        response = requests.put(
            f"{FASTAPI_URL}/auth/change_password",
            json=data,
            headers=get_auth_headers(request)
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")

        if response.status_code == 200:
            return redirect("profile")

        return render(
            request,
            "users/change_password.html",
            {
                "error": response.json().get("detail")
            }
        )

    return render(
        request,
        "users/change_password.html"
    )