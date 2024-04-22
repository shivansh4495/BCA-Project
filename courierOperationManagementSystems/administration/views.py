from django.shortcuts import render

# Create your views here.
def admin_login_form(request):
    return render(request, 'admin_login_form.html')