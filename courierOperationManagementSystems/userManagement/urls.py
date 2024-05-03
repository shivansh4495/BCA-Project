from django.urls import path, include
from . import views

app_name = 'userManagement'

urlpatterns = [
    path('user_login_form/', views.user_login_form, name='user_login_form'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('signup/', views.signup, name='signup'),
    path('client_order/', views.client_order, name='client_order'),
    path('calculate-distance/', views.calculate_distance_view, name='calculate_distance'),
]
