from django.urls import path
from . import views

app_name = 'BranchesInfo'
urlpatterns = [
    path('branch_login_form/', views.branch_login_form, name='branch_login_form'),
    path('branch_head_dashboard/', views.branch_head_dashboard, name='branch_head_dashboard'),
    path('delivery_boy_dashboard/', views.delivery_boy_dashboard, name='delivery_boy_dashboard'),
    path('add_delivery_boy/', views.add_delivery_boy, name='add_delivery_boy'),
    path('packet_assignment_details/', views.packet_assignment_details, name='packet_assignment_details'),
    path('delete_order/<str:awbno>/', views.delete_order, name='delete_order'),
    path('update_packet_status/', views.update_packet_status, name='update_packet_status'), 
]