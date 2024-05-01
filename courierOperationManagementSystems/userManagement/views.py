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
from django.utils import timezone
from django.db import connection

def user_login_form(request):
    if request.method == 'POST':
        username = request.POST.get('userid')
        password = request.POST.get('password')
        try:
            # Attempt to retrieve the Login_Info object
            login_info = Login_Info.objects.get(User_Id=username, User_Password=password)
            # Attempt to retrieve the corresponding Client object
            try:
                client = Client.objects.get(Client_Email_Id=username)
            except Client.DoesNotExist:
                # Handle the case where no corresponding Client exists for the provided email
                messages.error(request, 'Login failed: Invalid User name or Password')
                return render(request, 'User_login_form.html')
            # Set session data
            request.session['Client_Id'] = client.Client_Id
            request.session['Client_Name'] = client.Client_Name
            print("Session keys 'Client ID:' set successfully: ", client.Client_Id)
            print("Session keys 'Client_Name' set successfully for:", username)  
            # Render user dashboard page with username
            return render(request, 'user_dashboard.html', {'username': username})
        
        except Login_Info.DoesNotExist:
            # Handle invalid username or password
            print("Login failed: Invalid User name or Password")
            messages.error(request, 'Login failed: Invalid User name or Password')
    # Render login form
    return render(request, 'User_login_form.html')



def logout_view(request):
    logout(request)
    request.session.flush()  # Delete the session data
    print("Session deleted after logout:", request.session.session_key)
    return redirect('admin_login_form')  # Redirect to the login page after logout


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_dashboard(request):
    # Retrieve Client_Id from session
    client_id = request.session.get('Client_Id')
    print(client_id)

    # Retrieve orders associated with the current user
    user_orders = Data_Records.objects.filter(client__Client_Id=client_id)

    # Print the generated SQL query
    print(str(user_orders.query))

    # Pass user_orders to the template
    return render(request, 'user_dashboard.html', {'user_orders': user_orders})



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




def client_order(request):
    client_id = request.session.get('Client_Id')
    print("Session key 'Client_Id' value:", client_id)
    
    # Check if the session is valid (Client_Id exists in the session)
    if client_id:
        try:
            # Retrieve the client using Client_Email_Id
            client = Client.objects.get(Client_Id=client_id)
        except Client.DoesNotExist:
            # Handle the case where the client does not exist
            return render(request, 'User_login_form.html') # Redirect to login page

        if request.method == 'POST':
            sender_name = request.POST['sender_name']
            sender_address = request.POST['sender_address']
            sender_contact = request.POST['sender_contact']
            order_type = request.POST['order_type']
            order_date = request.POST['order_date'] 
            order_date_aware = timezone.make_aware(order_date)
            sender_city = request.POST['sender_city']
            sender_state = request.POST['sender_state']
            
            receiver_name = request.POST['receiver_name']
            receiver_address = request.POST['receiver_address']
            receiver_contact = request.POST['receiver_contact']
            receiver_city = request.POST['receiver_city']
            receiver_state = request.POST['receiver_state']
            payment_method = request.POST.get('payment_method')
            
            if payment_method == 'card':
                #! implement the payment gateway 
                pass
            
            elif payment_method == 'netbanking':
                #! implement the payment gateway 
                pass
            
            elif payment_method == 'upi':
                #! implement the payment gateway 
                pass
            
            elif payment_method == 'cash':
                # Save the order with the client ID
                final_order = Data_Records(Sender_Name=sender_name, Sender_Address=sender_address, Sender_Contact_No=sender_contact, Book_date=order_date_aware, Sender_City=sender_city, Receiver_Name=receiver_name, Receiver_Address=receiver_address, Receiver_Contact_No=receiver_contact, Receiver_City=receiver_city, order_type=order_type, sender_state=sender_state, receiver_state=receiver_state, Client_Id=client)
                final_order.save()
                return render(request, 'user_dashboard.html')
        else:
            current_date = datetime.now().strftime('%Y-%m-%d')
            sender_states = Branches.objects.values_list('state', flat=True).distinct()
            receiver_states = Branches.objects.values_list('state', flat=True).distinct()
            sender_cities = Branches.objects.values_list('city', flat=True).distinct()
            receiver_cities = Branches.objects.values_list('city', flat=True).distinct()
            return render(request, 'client_order.html', {'order_date': current_date, 'sender_cities': sender_cities, 'receiver_cities': receiver_cities, 'receiver_states': receiver_states, 'sender_states': sender_states})
    else:
        # If the session is not valid (Client_Id is not in the session), redirect to login page
        return render(request, 'User_login_form.html')
