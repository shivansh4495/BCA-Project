from django.shortcuts import render, redirect, reverse
#~ user authentication imports from django, apr 22
from . models import Client
from django.contrib import messages
from datetime import date

# Create your views here.
def user_login_form(request):
    return render(request, 'user_login_form.html')

def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def signup(request):
    return render(request, 'signup.html')