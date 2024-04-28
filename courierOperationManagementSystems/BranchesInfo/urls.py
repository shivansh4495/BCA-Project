from django.urls import path
from . import views

urlpatterns = [
    path('branch_login_form/', views.branch_login_form, name='branch_login_form'),
]