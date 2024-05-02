from django.shortcuts import render, redirect, reverse
from .models import Branch_head, delivery_Boy_details, Data_Records, Branches, PacketAssignmentDetails
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout

from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404 

# Create your views here.
def branch_login_form(request):
    if request.method == "POST":
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        user_type = request.POST.get('User_Type')
        
        # Check if the user type is selected
        if not user_type:
            messages.error(request, 'Please select a user type.')
            return render(request, "branch_login_form.html")
        
        if user_type == 'delivery_boy':
            # Check if the user exists in the delivery_Boy_details model
            delivery_boy = delivery_Boy_details.objects.filter(Delivery_Boy_Username=userid, Delivery_Boy_Password=password).first()
            if delivery_boy:
                request.session['Delivery_Boy_Id'] = delivery_boy.Delivery_Boy_Id
                request.session['userid'] = delivery_boy.Delivery_Boy_Username
                print("Session keys 'Delivery_Boy_Id' and 'delivery boy name' set successfully: ", delivery_boy.Delivery_Boy_Id, delivery_boy.Delivery_Boy_Username)
                return redirect(reverse('BranchesInfo:delivery_boy_dashboard') + f'?username={delivery_boy.Delivery_Boy_Username}')
            else:
                messages.error(request, 'Invalid delivery boy credentials.')
        
        elif user_type == 'branch_head':
            # Check if the user exists in the Branch_head model
            branch_head = Branch_head.objects.filter(Branch_head_Username=userid, Branch_head_Password=password).first()
            if branch_head:
                request.session['Branch_head_Id'] = branch_head.Branch_head_Id
                request.session['userid'] = branch_head.Branch_head_Username
                print("Session keys 'Branch_head_Id' and 'branch head name' set successfully: ", branch_head.Branch_head_Id, branch_head.Branch_head_Username)
                return redirect(reverse('BranchesInfo:branch_head_dashboard') + f'?username={branch_head.Branch_head_Username}')
            else:
                messages.error(request, 'Invalid branch head credentials.')
        
        # If user does not exist in either model, display error message
        messages.error(request, 'Invalid User or User Type')
    
    return render(request, "branch_login_form.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('branch_login_form')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def branch_head_dashboard(request):
    # Retrieve the username from the query parameters
    username = request.GET.get('username')
    # You may need to adjust this if the username is not passed in the query parameters
    if username:
        try:
            session_id = request.session.get('Branch_head_Id')
            if session_id is not None:
                print("Session ID of the branch head from dashboard function:", session_id)
                # Fetch data related to the branch head and pass it to the dashboard template
                # Here you can fetch any data related to the branch head
                return render(request, 'branch_head_dashboard.html', {'username': username})
        except KeyError:
            print("Session key not found")
    # Redirect to the login form if session is not available or invalid
    return redirect(reverse('BranchesInfo:branch_login_form'))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delivery_boy_dashboard(request):
    # Retrieve the username from the query parameters
    username = request.GET.get('username')
    # You may need to adjust this if the username is not passed in the query parameters
    if username:
        try:
            session_id = request.session.get('Delivery_Boy_Id')
            if session_id is not None:
                print("Session ID of the delivery boy:", session_id)
                # Fetch data related to the delivery boy and pass it to the dashboard template
                # Here you can fetch any data related to the delivery boy
                return render(request, 'delivery_boy_dashboard.html', {'username': username})
        except KeyError:
            print("Session key not found")
    # Redirect to the login form if session is not available or invalid
    return redirect(reverse('BranchesInfo:branch_login_form'))


def add_delivery_boy(request):
    if request.method == "POST":
        delivery_boy_name = request.POST.get('delivery_boy_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        area = request.POST.get('area')
        branch_cd = request.POST.get('branch_cd')
        User_Type='delivery_boy'

        # Create a new delivery boy object
        new_delivery_boy = delivery_Boy_details(
            Delivery_Boy_Name=delivery_boy_name,
            Delivery_Boy_Username=username,
            Delivery_Boy_Password=password,
            Delivery_Boy_Address=address,
            Delivery_Boy_contact_No=contact_no,
            Delivery_Boy_Area=area,
            Branch_CD=branch_cd,
            User_Type=User_Type
        )
        new_delivery_boy.save()
        messages.success(request, 'Delivery Boy Successfully.')
        
    return render(request, 'add_delivery_boy.html')  


def packet_assignment_details(request):
    if request.method == "POST":
        # Process form data if needed
        pass
    if 'Branch_head_Id' in request.session:
        
        branch_head_id = request.session['Branch_head_Id']
        
        sender_cities = Data_Records.objects.values_list('Sender_City', flat=True)
        return redirect(reverse('BranchesInfo:branch_head_dashboard')) 
    else:
        
        return redirect('BranchesInfo:branch_login_form') 
