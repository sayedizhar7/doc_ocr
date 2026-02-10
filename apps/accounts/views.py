from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model

from .forms import SignupForm, LoginForm

User = get_user_model()

@never_cache
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("pending")
    return render(request, "accounts/signup.html", {"form": form})

@never_cache
def pending_view(request):
    return render(request, "accounts/pending.html")

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if user.status != User.Status.APPROVED:
            messages.warning(request, "Your account is under progress. Kindly connect the admin.")
            return redirect("pending")
        login(request, user)
        return redirect("dashboard")

    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
