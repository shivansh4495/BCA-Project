from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Admin_table
from django.views.decorators.cache import cache_control
from BranchesInfo.models import Data_Records, Branches
from django.contrib.auth import logout, authenticate, login


def admin_login_form(request):
    if request.method == 'POST':
        username = request.POST['userid']
        password = request.POST['password']
        try:
            # obj = Admin_table.objects.get(Admin_Name=username, Admin_Password=password) 
            admin_table = Admin_table.objects.filter(Admin_Name=username, Admin_Password=password).first()
            # request.session['Admin_Id']=username
            request.session['Admin_Id'] = admin_table.Admin_Id  # Set the Admin_Id from the retrieved object
            request.session['username'] = admin_table.Admin_Name  
            print("Session key 'Admin_Id' set successfully:", admin_table.Admin_Id)  # For debugging
            
            print("Session key 'Admin_Id' set successfully:", admin_table.Admin_Name)  # Add this line for debugging
            # return render(request, 'admin_dashboard.html', {'username': username})
            return redirect(reverse('administration:admin_dashboard') + f'?username={admin_table.Admin_Name}')
        except Admin_table.DoesNotExist:
            print("Login failed: Invalid User name or Password")
            messages.success(request, 'Invalid User name or Password')
    return render(request, 'admin_login_form.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    return redirect('admin_login_form')  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    username = request.GET.get('username')
    if username:
        try:
            session_id = request.session.get('Admin_Id')
            if session_id is not None:
                print("Session ID of the branch head from dashboard function:", session_id)
                return render(request, 'admin_dashboard.html', {'username': username})
        except KeyError:
            print("Session key not found")
    return redirect(reverse('administration:admin_login_form'))



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    
    # Count the number of packets for each type
    courier_count = Data_Records.objects.filter(Type='Courier').count()
    cargo_count = Data_Records.objects.filter(Type='Cargo').count()
    logistics_count = Data_Records.objects.filter(Type='Logistics').count()
    context = {
        'courier_count': courier_count,
        'cargo_count': cargo_count,
        'logistics_count': logistics_count,
        'username': request.user.username,
    }
    return render(request, 'administration:admin_dashboard.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_branch(request):
    if request.method=="POST":
        branchName=request.POST['branchName']
        branchHead=request.POST['branchHead']
        address=request.POST['address']
        city=request.POST['city']
        cityId=request.POST['cityId']
        state=request.POST['state']
        stateId=request.POST['stateId']
        country=request.POST['country']
        countryId=request.POST['countryId']
        
        new_branch=Branches(Branch_NM=branchName, Branch_head=branchHead, Address=address, city=city, cityId=cityId, state=state, stateId=stateId, country=country, countryId=countryId)
        new_branch.save()
        messages.success(request,'branch saved')
    return render(request,"add_branch.html")


def ChargeDetails(request):
    return redirect(reverse('administration:ChargeDetails'))