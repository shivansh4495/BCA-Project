from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Admin_table
from django.views.decorators.cache import cache_control

# Create your views here.
# def admin_login_form(request):
#     return render(request, 'admin_login_form.html')

def admin_login_form(request):
    if request.method == 'POST':
        username = request.POST['userid']
        password = request.POST['password']
        try:
            obj = Admin_table.objects.get(Admin_Name=username, Admin_Password=password)
            request.session['Admin_Id']=username
            print("Session key 'Admin_Id' set successfully:", username)  # Add this line for debugging
            return render(request, 'admin_dashboard.html', {'username': username})
        except Admin_table.DoesNotExist:
            print("Login failed: Invalid User name or Password")
            messages.error(request, 'Invalid User name or Password')
    return render(request, 'admin_login_form.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    Admin_Id = request.session.get('Admin_Id')
    print("Session key 'Admin_Id' value:", Admin_Id)  # Add this line for debugging
    if Admin_Id:
        # Session key exists, do something with it
        admdetail = Admin_table.objects.get(Admin_Id=Admin_Id)
        return render(request, 'admin_dashboard.html', {'admdetail': admdetail})
    else:
        # Session key does not exist, handle the case accordingly
        return redirect('admin_login_form')
