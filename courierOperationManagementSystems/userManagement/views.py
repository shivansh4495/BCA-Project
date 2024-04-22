from django.shortcuts import render, redirect, reverse
#~ user authentication imports from django, apr 22
from django.contrib.auth import authenticate, login
from . models import Client, Login_Info
from django.contrib import messages
from datetime import date
from . forms import MyForm

# Create your views here.
# def user_login_form(request):
#     return render(request, 'user_login_form.html')

def user_login_form(request):
    if request.method == 'POST':
        username = request.POST.get('userid')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard.html')  # Redirect to user_dashboard.html upon successful login
        else:
            # Handle invalid login credentials
            return render(request, 'user_login_form.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'user_login_form.html')


def user_dashboard(request):
    return render(request, 'user_dashboard.html')

# def signup(request):
#     return render(request, 'signup.html')

def signup(request):
    form=MyForm()   
    if request.method=="POST":
        form=MyForm(request.POST)
        if form.is_valid():
            Client_Name=request.POST['Client_Name']
            Client_Address=request.POST['Client_Address']
            Client_contact_No=request.POST['Client_contact_No']
            Client_Email_Id=request.POST['Client_Email_Id']
            password=request.POST['password']
            User_Type='client'
            new_client=Client(Client_Name=Client_Name, Client_Address=Client_Address, Client_contact_No=Client_contact_No, Client_Email_Id=Client_Email_Id)
            log=Login_Info( User_Id=Client_Email_Id,User_Password=password, User_Type=User_Type)
            new_client.save()
            log.save()
            messages.success(request,'Client is registered')
        else:
            messages.success(request,'Invalid captcha code')
    return render(request,"signup.html",locals())