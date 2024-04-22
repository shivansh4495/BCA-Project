from django.urls import path
from . import views

urlpatterns = [
    path('admin_login_form/', views.admin_login_form, name='admin_login_form'),
    # Other admin-related URLs
]
