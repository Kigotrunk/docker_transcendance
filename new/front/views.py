from django.shortcuts import render

from myaccount.models import Account

# Create your views here.

def home(request):
    return render(request, "front/home.html")

def profile(request):
    return render(request, "front/profile.html")

def game(request):
    return render(request, "front/game.html")

def chat(request):
    return render(request, "front/chat.html")
