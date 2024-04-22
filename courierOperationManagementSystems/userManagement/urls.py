from django.urls import path
from . import views

urlpatterns = [
    path('user_login_form/', views.user_login_form, name='user_login_form'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('signup/', views.signup, name='signup'),
    # Other user-related URLs
]
