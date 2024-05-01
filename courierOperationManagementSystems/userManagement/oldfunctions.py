
# client order

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def client_order(request):
#     # form=MyForm() 
#     if request.method == 'POST':
#         sender_name = request.POST['sender_name']
#         sender_address = request.POST['sender_address']
#         sender_contact = request.POST['sender_contact']
#         order_type = request.POST['order_type']
#         order_date = request.POST['order_date'] 
#         sender_city = request.POST['sender_city']
#         sender_state = request.POST['sender_state']
        
#         receiver_name = request.POST['receiver_name']
#         receiver_address = request.POST['receiver_address']
#         receiver_contact = request.POST['receiver_contact']
#         receiver_city = request.POST['receiver_city']
#         receiver_state = request.POST['receiver_state']
        
#         # Get the client's session ID for showing the orders to the correct user's dashboard.
#         client_id = request.session.get('Client_Id')
#         print("Session key 'Client_Id' value:", client_id)
        
#         # Save the form data to Data_Records table
#         final_order = Data_Records(Sender_Name=sender_name, Sender_Address=sender_address, Sender_Contact_No=sender_contact, Book_date=order_date, Sender_City=sender_city, Receiver_Name=receiver_name, Receiver_Address=receiver_address, Receiver_Contact_No=receiver_contact, Receiver_City=receiver_city, order_type=order_type, receiver_state=receiver_state, sender_state=sender_state)
#         final_order.save()
#         return redirect('user_dashboard')
#     else:
#         current_date = datetime.now().strftime('%Y-%m-%d')
#         sender_states = Branches.objects.values_list('state', flat=True).distinct()
#         receiver_states = Branches.objects.values_list('state', flat=True).distinct()
#         # Fetch initial sender and receiver cities
#         sender_cities = Branches.objects.filter(state=sender_states[0]).values_list('city', flat=True).distinct()
#         receiver_cities = Branches.objects.filter(state=receiver_states[0]).values_list('city', flat=True).distinct()

#         # sender_cities = Branches.objects.values_list('city', flat=True).distinct()
#         # receiver_cities = Branches.objects.values_list('city', flat=True).distinct()
        
#         return render(request, 'client_order.html', {'order_date': current_date,'sender_states': sender_states ,'sender_cities': sender_cities, 'receiver_states':receiver_states ,'receiver_cities': receiver_cities})
