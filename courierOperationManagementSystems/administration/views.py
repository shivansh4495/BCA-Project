from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Admin_table
from django.views.decorators.cache import cache_control 
from BranchesInfo.models import Data_Records, Branches, Branch_head
from BranchesInfo.models import ChargeDetails
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from .forms import BranchForm, ChargeDetailsForm, BranchHeadForm
from django.http import HttpResponseNotAllowed


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login_form(request):
    if request.method == 'POST':
        username = request.POST['userid']
        password = request.POST['password']
        try:
            admin_table = Admin_table.objects.filter(Admin_Name=username, Admin_Password=password).first()
            request.session['Admin_Id'] = admin_table.Admin_Id  
            request.session['username'] = admin_table.Admin_Name  
            print("Session key 'Admin_Id' set successfully:", admin_table.Admin_Id)  
            
            print("Session key 'Admin_Id' set successfully:", admin_table.Admin_Name) 
            return redirect(reverse('administration:admin_dashboard') + f'?username={admin_table.Admin_Name}')
        except Admin_table.DoesNotExist:
            print("Login failed: Invalid User name or Password")
            messages.error(request, 'Invalid User name or Password')
            return render(request, 'admin_login_form.html', {'error_message': 'Invalid User name or Password'})
        except Exception as e:
            print("An error occurred:", str(e))
            messages.error(request, 'An error occurred. Please try again later.')
            return render(request, 'admin_login_form.html', {'error_message': 'An error occurred. Please try again later.'})
    return render(request, 'admin_login_form.html')


def logout_view(request):
    try:
        # Check if the keys exist in the session before deletion
        print("Session keys before deletion:", request.session.keys())

        if 'Admin_Id' in request.session:
            print("Admin_Id in session:", request.session['Admin_Id'])
        else:
            print("Admin_Id not found in session")
        
        if 'username' in request.session:
            print("username in session:", request.session['username'])
        else:
            print("username not found in session")

        # Delete the session keys
        del request.session['Admin_Id']
        del request.session['username']
        print("Session keys deleted")

        # Redirect after logout
        return redirect('administration:admin_login_form')
    except KeyError as e:
        print("Error deleting session keys:", e)
        return redirect('administration:admin_login_form')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    username = request.GET.get('username')
    if username:
        try:
            session_id = request.session.get('Admin_Id')
            if session_id is not None:
                print("Session ID of the branch head from dashboard function:", session_id)
                branches = Branches.objects.all().values()
                total_branches = branches.count()
                courier_count = Data_Records.objects.filter(order_type='courier').count()
                cargo_count = Data_Records.objects.filter(order_type='cargo').count()
                logistics_count = Data_Records.objects.filter(order_type='logistics').count()
                charge_details = ChargeDetails.objects.all()
                context = {
                    'courier_count': courier_count,
                    'cargo_count': cargo_count,
                    'logistics_count': logistics_count,
                    'username': username,
                    'total_branches': total_branches,
                    'branches': branches,
                    'charge_details': charge_details,
                }
                return render(request, 'admin_dashboard.html', context)
        except KeyError:
            print("Session key not found")
    return redirect(reverse('administration:admin_login_form'))


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



def edit_branch(request, branch_id):
    branch = get_object_or_404(Branches, Branch_CD=branch_id)
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('administration:admin_dashboard')
    else:
        form = BranchForm(instance=branch)
    return render(request, 'edit_branch.html', {'form': form, 'branch': branch})



def delete_branch(request, branch_id):
    branch = get_object_or_404(Branches, Branch_CD=branch_id)
    if request.method == 'POST':
        branch.delete()
        return redirect('administration:admin_dashboard')
    return render(request, 'confirm_delete.html', {'branch': branch})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def charge_details_view(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        # distance = request.POST.get('distance')
        weight = request.POST.get('weight')
        amount = request.POST.get('amount')
        
        print("Description:", description)
        # print("Distance:", distance)
        print("Weight:", weight)
        print("Amount:", amount)
        try:
            new_charge_details = ChargeDetails.objects.create(
                Description=description,
                # Distance=distance,
                Weight=weight,
                Amount=amount
            )
            messages.success(request, "Charge details added successfully!")
            print("New ChargeDetails object created successfully:", new_charge_details)
        except Exception as e:
            print("Error creating ChargeDetails object:", e)
        return redirect(reverse('administration:ChargeDetails'))
    return render(request, 'ChargeDetails.html')

# Edit charge detail
def edit_charge_detail(request, charge_id):
    charge_detail = get_object_or_404(ChargeDetails, pk=charge_id)
    if request.method == 'POST':
        form = ChargeDetailsForm(request.POST, instance=charge_detail)
        if form.is_valid():
            form.save()
            return redirect('administration:admin_dashboard')
    else:
        form = ChargeDetailsForm(instance=charge_detail)
    return render(request, 'edit_charge_detail.html', {'form': form, 'charge_detail': charge_detail})

# Delete charge detail
def delete_charge_detail(request, charge_id):
    charge_detail = get_object_or_404(ChargeDetails, pk=charge_id)
    if request.method == 'POST':
        charge_detail.delete()
        return redirect('administration:admin_dashboard')
    return render(request, 'confirm_delete_charge_detail.html', {'charge_detail': charge_detail})

def add_branch_head(request):
    if request.method == 'POST':
        form = BranchHeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration:admin_dashboard')  
    else:
        form = BranchHeadForm()
    return render(request, 'add_branch_head.html', {'form': form})
