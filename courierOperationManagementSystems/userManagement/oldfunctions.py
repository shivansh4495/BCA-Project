# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def client_order(request):
#     client_id = request.session.get('Client_Id')
#     print("Session key 'Client_Id' value:", client_id)
    
#     # Check if the session is valid (Client_Id exists in the session)
#     if client_id:
#         try:
#             # Retrieve the client using Client_Email_Id
#             client = Client.objects.get(Client_Id=client_id)
#         except Client.DoesNotExist:
#             # Handle the case where the client does not exist
#             return render(request, 'User_login_form.html') # Redirect to login page
#         if request.method == 'POST':
#             sender_name = request.POST['sender_name']
#             sender_address = request.POST['sender_address']
#             sender_contact = request.POST['sender_contact']
#             order_type = request.POST['order_type']
#             order_date = request.POST['order_date']
#             order_time = request.POST['order_time']  # Retrieve time separately
#             order_datetime_str = f"{order_date}T{order_time}"  # Combine date and time
#             order_date_aware = timezone.make_aware(datetime.strptime(order_datetime_str, "%Y-%m-%dT%H:%M")) 
#             sender_city = request.POST['sender_city']
#             sender_state = request.POST['sender_state']
            
#             receiver_name = request.POST['receiver_name']
#             receiver_address = request.POST['receiver_address']
#             receiver_contact = request.POST['receiver_contact']
#             receiver_city = request.POST['receiver_city']
#             receiver_state = request.POST['receiver_state']
#             payment_method = request.POST.get('payment_method')
            
#             if payment_method == 'card':
#                 #! implement the payment gateway 
#                 pass
            
#             elif payment_method == 'netbanking':
#                 #! implement the payment gateway 
#                 pass
            
#             elif payment_method == 'upi':
#                 #! implement the payment gateway 
#                 pass
            
#             elif payment_method == 'cash':
#                 # Save the order with the client ID
#                 final_order = Data_Records(Sender_Name=sender_name, Sender_Address=sender_address, Sender_Contact_No=sender_contact, Book_date=order_date_aware, Sender_City=sender_city, Receiver_Name=receiver_name, Receiver_Address=receiver_address, Receiver_Contact_No=receiver_contact, Receiver_City=receiver_city, order_type=order_type, sender_state=sender_state, receiver_state=receiver_state, Client_Id=client)
#                 final_order.save()
#                 return redirect('userManagement:user_dashboard')
#         else:
#             # current_date = datetime.now().strftime('%Y-%m-%d')  
#             sender_states = Branches.objects.values_list('state', flat=True).distinct()
#             receiver_states = Branches.objects.values_list('state', flat=True).distinct()
#             sender_cities = Branches.objects.values_list('city', flat=True).distinct()
#             receiver_cities = Branches.objects.values_list('city', flat=True).distinct()
#             return render(request, 'client_order.html', {'sender_cities': sender_cities, 'receiver_cities': receiver_cities, 'receiver_states': receiver_states, 'sender_states': sender_states})
#     else:
#         # If the session is not valid (Client_Id is not in the session), redirect to login page
#         return render(request, 'User_login_form.html')





#~ new old function

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def client_order(request):
#     client_id = request.session.get('Client_Id')
#     print("Session key 'Client_Id' value:", client_id)
    
#     # Check if the session is valid (Client_Id exists in the session)
#     if client_id:
#         try:
#             # Retrieve the client using Client_Email_Id
#             client = Client.objects.get(Client_Id=client_id)
#         except Client.DoesNotExist:
#             # Handle the case where the client does not exist
#             return render(request, 'User_login_form.html') # Redirect to login page
        
#         if request.method == 'POST':
#             sender_name = request.POST['sender_name']
#             sender_address = request.POST['sender_address']
#             sender_contact = request.POST['sender_contact']
#             order_type = request.POST['order_type']
#             order_date = request.POST['order_date']
#             order_time = request.POST['order_time']  # Retrieve time separately
#             order_datetime_str = f"{order_date}T{order_time}"  # Combine date and time
#             order_date_aware = timezone.make_aware(datetime.strptime(order_datetime_str, "%Y-%m-%dT%H:%M")) 
#             sender_city = request.POST['sender_city']
#             sender_state = request.POST['sender_state']
            
#             receiver_name = request.POST['receiver_name']
#             receiver_address = request.POST['receiver_address']
#             receiver_contact = request.POST['receiver_contact']
#             receiver_city = request.POST['receiver_city']
#             receiver_state = request.POST['receiver_state']
#             payment_method = request.POST.get('payment_method')
            
#             if payment_method == 'card':
#                 #! implement the payment gateway 
#                 pass
            
#             elif payment_method == 'netbanking':
#                 #! implement the payment gateway 
#                 pass
            
#             elif payment_method == 'upi':
#                 #! implement the payment gateway 
#                 pass
            
#             elif payment_method == 'cash':
#                 # Calculate distance using Google Maps API
#                 gmaps = googlemaps.Client(key='YOUR_GOOGLE_MAPS_API_KEY')  # Replace with your API key
#                 sender_address_str = f"{sender_address}, {sender_city}, {sender_state}"
#                 receiver_address_str = f"{receiver_address}, {receiver_city}, {receiver_state}"
                
#                 # Get distance matrix between sender and receiver addresses
#                 distance_matrix = gmaps.distance_matrix(sender_address_str, receiver_address_str)
                
#                 if distance_matrix['status'] == 'OK':
#                     # Extract distance from response
#                     distance_value = distance_matrix['rows'][0]['elements'][0]['distance']['value']  # Distance in meters
#                     distance_km = distance_value / 1000  # Convert meters to kilometers
                    
#                     # Save the order with the client ID
#                     final_order = Data_Records(
#                         Sender_Name=sender_name, Sender_Address=sender_address, Sender_Contact_No=sender_contact,
#                         Book_date=order_date_aware, Sender_City=sender_city, Receiver_Name=receiver_name,
#                         Receiver_Address=receiver_address, Receiver_Contact_No=receiver_contact,
#                         Receiver_City=receiver_city, order_type=order_type, sender_state=sender_state,
#                         receiver_state=receiver_state, Client_Id=client, Distance=distance_km)
#                     final_order.save()
#                     return redirect('userManagement:user_dashboard')
#                 else:
#                     # Handle error response from Google Maps API
#                     messages.error(request, 'Error retrieving distance between addresses from Google Maps API.')
#                     return redirect('userManagement:user_dashboard')
#         else:
#             # current_date = datetime.now().strftime('%Y-%m-%d')  
#             sender_states = Branches.objects.values_list('state', flat=True).distinct()
#             receiver_states = Branches.objects.values_list('state', flat=True).distinct()
#             sender_cities = Branches.objects.values_list('city', flat=True).distinct()
#             receiver_cities = Branches.objects.values_list('city', flat=True).distinct()
#             return render(request, 'client_order.html', {'sender_cities': sender_cities, 'receiver_cities': receiver_cities, 'receiver_states': receiver_states, 'sender_states': sender_states})
#     else:
#         # If the session is not valid (Client_Id is not in the session), redirect to login page
#         return render(request, 'User_login_form.html')