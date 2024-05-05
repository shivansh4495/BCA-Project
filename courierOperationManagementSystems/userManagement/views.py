from django.shortcuts import render, redirect, reverse
from . models import Client, Login_Info
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from . forms import MyForm
from packetTrackingSystem.models import User_Info
from BranchesInfo.models import Data_Records, Branches, ChargeDetails
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout
from django.utils import timezone
import googlemaps
import json
from django.http import JsonResponse


def user_login_form(request):
    if request.method == 'POST':
        username = request.POST.get('userid')
        password = request.POST.get('password')
        try:
            login_info = Login_Info.objects.get(User_Id=username, User_Password=password)
            client = Client.objects.get(Client_Email_Id=username)
            request.session['Client_Name'] = client.Client_Name
            request.session['Client_Id'] = client.Client_Id
            print("Session keys 'Client ID:' set successfully: ", client.Client_Id)
            return redirect(reverse('userManagement:user_dashboard') + f'?username={client.Client_Name}')
        except Login_Info.DoesNotExist:
            print("Login failed: Invalid User name or Password")
            messages.error(request, 'Login failed: Invalid User name or Password')
    return render(request, 'User_login_form.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_dashboard(request):
    # Retrieve the username from the query parameters
    username = request.GET.get('username')
    try:
        session_id = request.session.get('Client_Id')
        if session_id is not None:
            print("Session ID of the user :", session_id)
            # Fetch data related to the user and pass it to the dashboard template
            user_orders = Data_Records.objects.filter(Client_Id=session_id)
            return render(request, 'user_dashboard.html', {'user_orders': user_orders, 'username': username})
    except KeyError:
        print("Session key not found")
    # Redirect to the login form if session is not available or invalid
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
            order_time = request.POST['order_time']  # Retrieve time separately
            order_datetime_str = f"{order_date}T{order_time}"  # Combine date and time
            order_date_aware = timezone.make_aware(datetime.strptime(order_datetime_str, "%Y-%m-%dT%H:%M")) 
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
                return redirect('userManagement:user_dashboard')
        else:
            # current_date = datetime.now().strftime('%Y-%m-%d')  
            sender_states = Branches.objects.values_list('state', flat=True).distinct()
            receiver_states = Branches.objects.values_list('state', flat=True).distinct()
            sender_cities = Branches.objects.values_list('city', flat=True).distinct()
            receiver_cities = Branches.objects.values_list('city', flat=True).distinct()
            return render(request, 'client_order.html', {'sender_cities': sender_cities, 'receiver_cities': receiver_cities, 'receiver_states': receiver_states, 'sender_states': sender_states})
    else:
        # If the session is not valid (Client_Id is not in the session), redirect to login page
        return render(request, 'User_login_form.html')


def calculate_distance(sender_address, receiver_address, api_key):
    gmaps = googlemaps.Client(key=api_key)
    # Call the distance_matrix method to calculate the distance
    result = gmaps.distance_matrix(sender_address, receiver_address)
    if 'rows' in result and result['rows']:
        distance = result['rows'][0]['elements'][0]['distance']['value']
        distance_in_km = round(distance / 1000, 1)  # Convert distance from meters to kilometers and round to nearest tenth
        return distance_in_km
    else:
        return None

def calculate_distance_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sender_address = data.get('sender_address')
        receiver_address = data.get('receiver_address')
        api_key = 'AIzaSyAq23BWf_3ZAOZvqyGZlUzfaOA9WrgUk_w'   #! Remember to remove your API key, daily limit 100 requests after that charges will apply
        distance = calculate_distance(sender_address, receiver_address, api_key)
        if distance is not None:
            return JsonResponse({'distance': distance})
        else:
            return JsonResponse({'error': 'Failed to retrieve distance.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)



def calculate_price_view(request):
    if request.method == 'POST':
        # Get weight from POST data
        weight = float(request.POST.get('weight'))

        # Fetch distance from the calculate_distance_view function
        # Assuming the endpoint is named 'calculate_distance_view' and accessible via POST request
        distance_response = calculate_distance_view(request)
        if distance_response.status_code == 200:
            distance_data = distance_response.json()
            distance = distance_data.get('distance')
        else:
            return JsonResponse({'error': 'Failed to calculate distance.'}, status=400)

        # Fetch the ChargeDetails object based on the weight
        charge_details = ChargeDetails.objects.filter(Weight__gte=weight).order_by('Weight').first()
        
        if charge_details:
            price_per_km = charge_details.Amount
            # Calculate the total price based on distance and price per kilometer
            total_price = distance * price_per_km
            return JsonResponse({'total_price': total_price})
        else:
            return JsonResponse({'error': 'Failed to calculate price.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


def logout_view(request):
    logout(request)
    request.session.flush()  # Delete the session data
    print("Session deleted after logout:", request.session.session_key)
    return redirect('admin_login_form')  # Redirect to the login page after logout
