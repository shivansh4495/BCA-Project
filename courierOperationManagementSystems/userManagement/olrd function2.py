# def user_login_form(request):
#     if request.method == 'POST':
#         username = request.POST.get('userid')
#         password = request.POST.get('password')
#         try:
#             login_info = Login_Info.objects.get(User_Id=username, User_Password=password)
#             client = Client.objects.get(Client_Email_Id=username)
#             request.session['Client_Name'] = client.Client_Name
#             request.session['Client_Id'] = client.Client_Id
#             print("Session keys 'Client ID:' set successfully: ", client.Client_Id)
#             return redirect(reverse('userManagement:user_dashboard') + f'?username={client.Client_Name}')
#         except Login_Info.DoesNotExist:
#             print("Login failed: Invalid User name or Password")
#             messages.error(request, 'Login failed: Invalid User name or Password')
#     return render(request, 'User_login_form.html')



# def user_dashboard(request):
#     # Retrieve the username from the query parameters
#     username = request.GET.get('username')
#     try:
#         session_id = request.session.get('Client_Id')
#         if session_id is not None:
#             print("Session ID of the user :", session_id)
#             # Fetch data related to the user and pass it to the dashboard template
#             user_orders = Data_Records.objects.filter(Client_Id=session_id)
            
#             # Fetch live updates related to the user's orders
#             live_updates = Live_Updates.objects.filter(AWBNO__in=[order.AWBNO for order in user_orders])
#             return render(request, 'user_dashboard.html', {'user_orders': user_orders, 'username': username, 'live_updates': live_updates})
#     except KeyError:
#         print("Session key not found")
#     # Redirect to the login form if session is not available or invalid
#     return redirect('user_login_form')


# def profile_management(request):
#     client_id = request.session.get('Client_Id')
#     client = Client.objects.get(Client_Id=client_id)
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=client)
#         if form.is_valid():
#             form.save()
#             # Update the session with the new client name after the profile update
#             request.session['Client_Name'] = form.cleaned_data['Client_Name']
#             return redirect('userManagement:user_dashboard')
#     else:
#         form = ProfileForm(instance=client)
#     return render(request, 'profile_management.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     request.session.flush() 
#     print("Session deleted after logout:", request.session.session_key)
#     return redirect('admin_login_form')