from django.shortcuts import render, redirect
from .models import Branch_head, delivery_Boy_details, Data_Records, Branches, PacketAssignmentDetails
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout
from django.urls import reverse
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404 
from .forms import PacketAssignmentForm
from .models import PacketAssignmentDetails
from packetTrackingSystem.models import Qr_Details, Live_Updates


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


def branch_head_dashboard(request):
    username = request.GET.get('username')
    if username:
        try:
            session_id = request.session.get('Branch_head_Id')
            if session_id is not None:
                print("Session ID of the branch head from dashboard function:", session_id)
                branch_head = Branch_head.objects.get(Branch_head_Username=username)
                branch_cd = branch_head.Branch_CD
                
                # Fetch the branch from the Branches table using the branch code
                branch = Branches.objects.get(Branch_CD=branch_cd)
                
                # Get the city of the branch
                branch_city = branch.city
                
                # Retrieve orders from Data_Records where sender city matches the branch city
                matching_orders = Data_Records.objects.filter(Sender_City=branch_city)
                
                # delivery_boys = delivery_Boy_details.objects.filter(Branch_CD=branch_cd)
                delivery_boys = delivery_Boy_details.objects.all()
                
                return render(request, 'branch_head_dashboard.html', {'username': username, 'orders': matching_orders, 'delivery_boys':delivery_boys})
        except KeyError:
            print("Session key not found")
    # Redirect to the login form if session is not available or invalid
    return redirect(reverse('BranchesInfo:branch_login_form'))

def delete_order(request, awbno):
    if request.method == 'POST':
        try:
            order = Data_Records.objects.get(AWBNO=awbno)
            order.delete()
            username = request.GET.get('username')
            return redirect(reverse('BranchesInfo:branch_head_dashboard') + '?username=' + username)
        except Data_Records.DoesNotExist:
            return HttpResponseNotFound("Order does not exist")
    else:
        return HttpResponseNotFound("Method not allowed")


def delivery_boy_dashboard(request):
    # Retrieve the username from the query parameters
    username = request.GET.get('username')
    # You may need to adjust this if the username is not passed in the query parameters
    if username:
        try:
            session_id = request.session.get('Delivery_Boy_Id')
            if session_id is not None:
                print("Session ID of the delivery boy:", session_id)
                delivery_boy = delivery_Boy_details.objects.get(Delivery_Boy_Username=username)
                packets_allotted = PacketAssignmentDetails.objects.filter(Delivery_Boy_Id=session_id)
                live_track = Live_Updates.objects.filter(Delivery_Boy_Name=username)
                packets_details = []
                qr_images = {}
                live_details =[]
                
                for packet in packets_allotted:
                    packet_details = Data_Records.objects.get(AWBNO=packet.AWBNO)
                    packets_details.append(packet_details)
                
                # # Fetch the QR code image for the packet
                    try:
                        qr_detail = Qr_Details.objects.get(awbno=packet.AWBNO)
                        qr_images[packet.AWBNO] = qr_detail.barcode_image.url
                    except Qr_Details.DoesNotExist:
                        qr_images[packet.AWBNO] = None
                for live in live_track:
                    live_details = {
                        'AWBNO': live.AWBNO,
                        'transit_status': live.transit_status,
                        'update_location': live.update_location,
                        'last_update_time': live.last_update_time,
                    }
                return render(request, 'delivery_boy_dashboard.html', {'username': username, 'delivery_boy': delivery_boy, 'packets_allotted': packets_allotted, 'packets_details': packets_details, 'live_track': live_track,'qr_images': qr_images})
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
    if request.method == 'POST':
        form = PacketAssignmentForm(request.POST)
        if form.is_valid():
            awbno = form.cleaned_data['awbno']
            delivery_boy = form.cleaned_data['delivery_boy']
            assignment = PacketAssignmentDetails(
                Delivery_Boy_Id=delivery_boy.Delivery_Boy_Id,
                AWBNO=awbno.AWBNO,
                Assign_DT=timezone.now()
            )
            assignment.save()
            messages.success(request, 'Packet allocated successfully.')
            return redirect('BranchesInfo:branch_head_dashboard')
    else:
        form = PacketAssignmentForm()
    return render(request, 'packet_assignment_details.html', {'form': form})

# def packet_reassignment(request, awbno):
#     packet = Data_Records.objects.get(AWBNO=awbno)
    
#     if request.method == 'POST':
#         form = PacketReassignmentForm(request.POST)
#         if form.is_valid():
#             new_delivery_boy = form.cleaned_data['delivery_boy']
#             # Update the assignment details for the packet
#             packet_assignment = PacketAssignmentDetails.objects.get(AWBNO=awbno)
#             packet_assignment.Delivery_Boy_Id = new_delivery_boy.Delivery_Boy_Id
#             packet_assignment.Assign_DT = timezone.now()
#             packet_assignment.save()
#             messages.success(request, 'Packet reassigned successfully.')
#             return redirect('BranchesInfo:branch_head_dashboard')
#     else:
#         form = PacketReassignmentForm(instance=packet)
#     return render(request, 'packet_reassignment.html', {'form': form})




def update_packet_status(request):
    delivery_boy_id = request.session.get('Delivery_Boy_Id')
    
    if request.method == 'POST':
        awbno = request.POST.get('awbno')
        transit_status = request.POST.get('transit_status')
        update_location = request.POST.get('update_location')
        order_update_time = timezone.now()

        # Get the delivery boy name from the session
        delivery_boy_name = delivery_Boy_details.objects.get(Delivery_Boy_Id=delivery_boy_id).Delivery_Boy_Username

        # Create and save the Order_Updates object
        orderUpdates = Live_Updates.objects.create(
            AWBNO=awbno,
            transit_status=transit_status,
            update_location=update_location,
            last_update_time=order_update_time,
            Delivery_Boy_Name=delivery_boy_name
        )

        # Redirect to the delivery boy dashboard
        return redirect(reverse('BranchesInfo:delivery_boy_dashboard'))

    return render(request, 'your_template.html')

