from functools import wraps
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if "token" not in request.session:
            return redirect("login")

        if request.session.get("role") != "admin":
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper