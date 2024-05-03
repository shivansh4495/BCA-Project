from django.urls import path, include
from . import views

app_name = 'administration'

urlpatterns = [
    path('admin_login_form/', views.admin_login_form, name='admin_login_form'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_branch/', views.add_branch, name='add_branch'),
    path('ChargeDetails/', views.charge_details_view, name='ChargeDetails'),
    path('ChargeDetails/', views.charge_details_view, name='ChargeDetails'),
    path('logout_view/', views.logout_view, name='logout_view'),
]
