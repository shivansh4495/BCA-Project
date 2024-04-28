from django.urls import path
from . import views

urlpatterns = [
    path('admin_login_form/', views.admin_login_form, name='admin_login_form'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # Other admin-related URLs
]
