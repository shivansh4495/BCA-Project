from django.shortcuts import render, redirect 
from django.urls import reverse
from . models import Client, Login_Info
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponseRedirect
from . forms import MyForm, ProfileForm
from packetTrackingSystem.models import User_Info, Live_Updates
from BranchesInfo.models import Data_Records, Branches, ChargeDetails
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout
from django.utils import timezone
import googlemaps
import json
from django.http import JsonResponse
from homeapp.models import Feedback
from .forms import FeedbackForm
from django.db import IntegrityError



def user_login_form(request):
    if request.method == 'POST':
        username = request.POST.get('userid')
        password = request.POST.get('password')
        try:
            login_info = Login_Info.objects.get(User_Id=username, User_Password=password)
            client = Client.objects.get(Client_Email_Id=username)
            if client.Client_Name:
                request.session['Client_Name'] = client.Client_Name
                request.session['Client_Id'] = client.Client_Id
                print("Session keys 'Client ID:' set successfully from login method: ", client.Client_Id)
                print("Session keys 'Client Name:' set successfully from login method: ", client.Client_Name)
                return redirect('userManagement:user_dashboard')
            else:
                print("Client name is empty for user:", username)
                messages.error(request, 'Client name is empty. Please contact support.')
        except Login_Info.DoesNotExist:
            print("Login failed: Invalid User name or Password")
            messages.error(request, 'Login failed: Invalid User name or Password')
    return render(request, 'user_login_form.html')



def user_dashboard(request):
    try:
        session_id = request.session.get('Client_Id')
        username = request.session.get('Client_Name')
        if session_id is not None:
            print("Session ID of the user from dashboard function :", session_id)
            print("Session username of the user from dashboard function :", username)
            user_orders = Data_Records.objects.filter(Client_Id=session_id)
            
            
            live_updates = Live_Updates.objects.filter(AWBNO__in=[order.AWBNO for order in user_orders]).order_by('-last_update_time')
            return render(request, 'user_dashboard.html', {'user_orders': user_orders, 'username': username, 'live_updates': live_updates})
    except KeyError:
        print("Session key not found")
    
    return redirect('userManagement:user_login_form')


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
            try:
                
                new_client.save()
                log.save()
                packet_table.save()
                messages.success(request,'Client is registered')
            except IntegrityError:
                messages.error(request, 'Email address already exists. Please use a different email address.')
        else:
            messages.success(request,'Invalid captcha code')
    return render(request,"signup.html",locals())

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def client_order(request):
    client_id = request.session.get('Client_Id')
    print("Session key 'Client_Id' value:", client_id)
    
    if client_id:
        try:
            
            client = Client.objects.get(Client_Id=client_id)
        except Client.DoesNotExist:
            
            return render(request, 'User_login_form.html') 
        if request.method == 'POST':
            sender_name = request.POST['sender_name']
            sender_address = request.POST['sender_address']
            sender_contact = request.POST['sender_contact']
            order_type = request.POST['order_type']
            order_date = request.POST['order_date']
            order_time = request.POST['order_time']  
            order_datetime_str = f"{order_date}T{order_time}"
            order_date_aware = timezone.make_aware(datetime.strptime(order_datetime_str, "%Y-%m-%dT%H:%M")) 
            sender_city = request.POST['sender_city']
            sender_state = request.POST['sender_state']
            weight = request.POST['weight']
            distance = request.POST['distance']
            receiver_name = request.POST['receiver_name']
            receiver_address = request.POST['receiver_address']
            receiver_contact = request.POST['receiver_contact']
            receiver_city = request.POST['receiver_city']
            receiver_state = request.POST['receiver_state']
            payment_method = request.POST.get('payment_method')
            total_price = request.POST['total_price']
            
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
                
                final_order = Data_Records(Sender_Name=sender_name, Sender_Address=sender_address, Sender_Contact_No=sender_contact, Book_date=order_date_aware, Sender_City=sender_city, Receiver_Name=receiver_name, Receiver_Address=receiver_address, Receiver_Contact_No=receiver_contact, Receiver_City=receiver_city, order_type=order_type, sender_state=sender_state, receiver_state=receiver_state, Client_Id=client, Weight=weight, Distance=distance, Price=total_price, Payment_Method=payment_method)
                final_order.save()
                return HttpResponseRedirect(reverse('userManagement:user_dashboard') + f'?username={client.Client_Name}')
        else:
            # current_date = datetime.now().strftime('%Y-%m-%d')  
            sender_states = Branches.objects.values_list('state', flat=True).distinct()
            receiver_states = Branches.objects.values_list('state', flat=True).distinct()
            sender_cities = Branches.objects.values_list('city', flat=True).distinct()
            receiver_cities = Branches.objects.values_list('city', flat=True).distinct()
            return render(request, 'client_order.html', {'sender_cities': sender_cities, 'receiver_cities': receiver_cities, 'receiver_states': receiver_states, 'sender_states': sender_states})
    else:
        
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
        api_key = ''   #! Important: Put your API key here.
        distance = calculate_distance(sender_address, receiver_address, api_key)
        if distance is not None:
            return JsonResponse({'distance': distance})
        else:
            return JsonResponse({'error': 'Failed to retrieve distance.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)



def calculate_price_view(request):
    if request.method == 'POST':
        weight = float(request.POST.get('weight'))
        distance_response = calculate_distance_view(request)
        if distance_response.status_code == 200:
            distance_data = distance_response.json()
            distance = distance_data.get('distance')
        else:
            return JsonResponse({'error': 'Failed to calculate distance.'}, status=400)
        charge_details = ChargeDetails.objects.filter(Weight__gte=weight).order_by('Weight').first()
        
        if charge_details:
            price_per_km = charge_details.Amount
            total_price = distance * price_per_km
            return JsonResponse({'total_price': total_price})
        else:
            return JsonResponse({'error': 'Failed to calculate price.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)



def profile_management(request):
    try:
        client_id = request.session.get('Client_Id')
        print(client_id)
        client = Client.objects.get(Client_Id=client_id)
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                return redirect('userManagement:user_dashboard')
        else:
            form = ProfileForm(instance=client)
        return render(request, 'profile_management.html', {'form': form})
    except KeyError:
        messages.error(request, 'Session data not found. Please log in again.')
        return redirect('userManagement:user_login_form')


def logout_view(request):
    try:
        session_id = request.session.get('Client_Id')
        session_name = request.session.get('Client_Name')
        if session_id and session_name:
            del request.session['Client_Id']
            del request.session['Client_Name']
            request.session.flush()
            print("Session data cleared successfully for logout_view:", session_name)
        logout(request)
        return redirect('userManagement:user_login_form')
    except Exception as e:
        print("Error occurred during logout:", e)
        return redirect('userManagement:user_login_form')


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the userDashboard after successful form submission
            return redirect('userManagement:user_dashboard')  
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

