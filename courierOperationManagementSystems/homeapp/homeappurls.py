from django.urls import path
from . import views

app_name = 'homeapp'

urlpatterns=[
    path('',views.home,name='home'),
    path('OrderTracking/', views.OrderTracking ,name='OrderTracking')
]