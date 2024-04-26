from django.shortcuts import render, redirect, reverse
from . models import Client, Login_Info
from django.contrib import messages
from datetime import date
from . forms import MyForm
from packetTrackingSystem.models import User_Info

# Create your views here.
# def user_login_form(request):
#     return render(request, 'user_login_form.html')

def user_login_form(request):
    if request.method == 'POST':
        username = request.POST('userid')
        password = request.POST('password')
        try:
            obj = Login_Info.objects.get(User_Id=username,User_Password=password)
            request.session['Client_Id']=username
            return redirect(reverse('user_dashboard.html'))
        except:
            messages.error(request, 'Invalid User name or Password')
    return render(request, 'user_login_form.html')

def user_dashboard(request):
    return render(request, 'user_dashboard.html')


# def user_dashboard(request):
#     try:
#         if request.session['Client_Id']!=None:
#             Client_Id=request.session['Client_Id']
#             usrdetail=User_Info.objects.get(User_Id=Client_Id)
#             return render(request,'studenthome.html',locals())
#     except KeyError:
#         return redirect('nouapp:login')


# def signup(request):
#     return render(request, 'signup.html')

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