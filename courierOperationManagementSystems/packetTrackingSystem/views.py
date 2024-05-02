from django.shortcuts import render, redirect, reverse
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from BranchesInfo.models import Data_Records



# Create your views here.





# def generate_qr_code(request, awbno):
#     packet = get_object_or_404(Data_Record, AWBNO=awbno)
#     qr_data = f"AWBNO: {packet.AWBNO}"  # Include AWBNO in the QR data
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(qr_data)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white")
#     img_bytes = BytesIO()
#     img.save(img_bytes, format='PNG')
#     return HttpResponse(img_bytes.getvalue(), content_type="image/png")

# def track_packet(request, awbno):
#     packet = get_object_or_404(Data_Record, AWBNO=awbno)
#     # You can return relevant information about the packet here
#     return HttpResponse(f"Tracking information for AWBNO {awbno}")