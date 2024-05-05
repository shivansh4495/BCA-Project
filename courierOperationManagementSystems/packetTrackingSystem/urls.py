from django.urls import path
from . import views
app_name = 'packetTrackingSystem'

urlpatterns = [
    path('generate-qr/', views.generate_and_store_barcode, name='generate_qr'),
]