from django.shortcuts import render, redirect, reverse
from . models import Client, Login_Info
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from . forms import MyForm
from packetTrackingSystem.models import User_Info
from BranchesInfo.models import Data_Records, Branches
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout


def user_login_form(request):
    if request.method == 'POST':
        username = request.POST['userid']
        password = request.POST['password']
        try:
            obj = Login_Info.objects.get(User_Id=username, User_Password=password)
            request.session['Client_Id']=username
            print("Session key 'Client_Id' set successfully:", username)  
            return render(request, 'user_dashboard.html', {'username': username})
        except Login_Info.DoesNotExist:
            print("Login failed: Invalid User name or Password")
            messages.error(request, 'Invalid User name or Password')
    return render(request, 'User_login_form.html')

def logout_view(request):
    logout(request)
    return redirect('admin_login_form')  # Redirect to the login page after logout


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_dashboard(request):
    client_id = request.session.get('Client_Id')
    print("Session key 'Client_Id' value:", client_id) 
    if client_id:
        # Session key exists, do something with it
        usrdetail = User_Info.objects.get(User_Id=client_id)
        return render(request, 'user_dashboard.html', {'usrdetail': usrdetail})
    else:
        # Session key does not exist, handle the case accordingly
        return redirect('user_login_form')


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
            packet_table=User_Info(User_Id=Client_Email_Id, User_Name=Client_Name, User_Address=Client_Address, User_contact_No=Client_contact_No, User_Email_Id=Client_Email_Id)
            new_client.save()
            log.save()
            packet_table.save()
            messages.success(request,'Client is registered')
        else:
            messages.success(request,'Invalid captcha code')
    return render(request,"signup.html",locals())

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def client_order(request):
    form=MyForm()
    if request.method == 'POST':
        sender_name = request.POST['sender_name']
        sender_address = request.POST['sender_address']
        sender_contact = request.POST['sender_contact']
        order_type = request.POST['order_type']
        order_date = request.POST['order_date'] 
        sender_city = request.POST['sender_city']
        
        receiver_name = request.POST['receiver_name']
        receiver_address = request.POST['receiver_address']
        receiver_contact = request.POST['receiver_contact']
        receiver_city = request.POST['receiver_city']
        
        # Get the client's session ID for showing the orders to the correct user's dashboard.
        client_id = request.session.get('Client_Id')
        print("Session key 'Client_Id' value:", client_id)
        
        # Save the form data to Data_Records table
        final_order = Data_Records(Sender_Name=sender_name, Sender_Address=sender_address, Sender_Contact_No=sender_contact, Book_date=order_date, Sender_City=sender_city, Receiver_Name=receiver_name, Receiver_Address=receiver_address, Receiver_Contact_No=receiver_contact, Receiver_City=receiver_city)
        final_order.save()
        return redirect('user_dashboard')
    else:
        current_date = datetime.now().strftime('%Y-%m-%d')
        sender_cities = Branches.objects.values_list('Address', flat=True).distinct()
        receiver_cities = Branches.objects.values_list('Address', flat=True).distinct()
        
        return render(request, 'client_order.html', {'order_date': current_date, 'sender_cities': sender_cities, 'receiver_cities': receiver_cities})
