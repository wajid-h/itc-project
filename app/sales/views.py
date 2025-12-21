from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Sale

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import error

# Create your views here.

def index(request):
    sales = Sale.objects.all()
    return render(request, "index.html", {"sales": sales})


def front_logout(request):
    logout(request)
    return redirect("login")


def onboard(request):
    print("preparing auth   ...")

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        action = request.POST.get("is_login")  # 'login' or 'signup' expected

        if action == "login":
            login_email = request.POST.get("login_email", "")
            login_password = request.POST.get("login_password", "")

            try:
                target_user = User.objects.get(email=login_email)
            except User.DoesNotExist:
                error(request, "No registered accounts with that email address.")
                return redirect("login")

            user = authenticate(request, username=target_user.username, password=login_password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                error(request, "Password entered for that account is invalid.")
                return redirect("login")

        elif action == "signup":
            fullName = request.POST.get("name", "").strip()
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "")
            conf_pass = request.POST.get("conf_password", "")

            if User.objects.filter(email=email).exists():
                error(request, "An account with that email exists. Perhaps you want to login?")
                return redirect("login")
            if User.objects.filter(username=username).exists():
                error(request, "That username is already in use.")
                return redirect("login")

            if password != conf_pass:
                error(request, "Passwords don't match.")
                return redirect("login")

            if len(password) < 5:
                error(request, "Password should be at least 5 characters long.")
                return redirect("login")

            new_user = User(email=email, first_name=fullName, username=username)
            new_user.set_password(conf_pass)
            new_user.save()

            # Authenticate then login to ensure backend is set
            user = authenticate(request, username=username, password=conf_pass)
            if user:
                login(request, user)
                return redirect('index')
            else:
                # fallback: if auth backend not found, try direct login
                login(request, new_user)
                return redirect('index')

    return render(request, "onboard.html")