from django.shortcuts import render

# Create your views here.
def branch_login_form(request):
    return render(request, 'branch_login_form.html')