import qrcode
from io import BytesIO
from django.core.files import File
from django.http import HttpResponse
from BranchesInfo.models import Data_Records
from .models import Qr_Details

def generate_and_store_barcode(request):
    if request.method == 'POST':
        awbno = request.POST.get('awbno')  # Retrieve awbno from the POST data
        try:
            # Fetch data from Data_Records based on AWBNO
            data_record = Data_Records.objects.get(AWBNO=awbno)

            # Generate QR code with data from Data_Records
            qr_data = f'Sender Name: {data_record.Sender_Name}\n'
            qr_data += f'Sender Address: {data_record.Sender_Address}\n'
            qr_data += f'Sender City: {data_record.Sender_City}\n'
            qr_data += f'Sender State: {data_record.sender_state}\n'
            qr_data += f'Receiver Name: {data_record.Receiver_Name}\n'
            qr_data += f'Receiver Address: {data_record.Receiver_Address}\n'
            qr_data += f'Receiver City: {data_record.Receiver_City}\n'
            qr_data += f'Receiver State: {data_record.receiver_state}\n'
            qr_data += f'Payment Method: {data_record.Payment_Method}\n'

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            # Create an in-memory binary stream
            buffer = BytesIO()

            # Save the QR code image to the buffer
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save(buffer)
            buffer.seek(0)

            # Create Qr_Details object and save the image
            qr_detail = Qr_Details()
            qr_detail.awbno = awbno  # Save the AWBNO
            qr_detail.barcode_image.save(f'barcode_{awbno}.png', File(buffer))
            qr_detail.save()

            return HttpResponse("Barcode generated and stored successfully.")
        except Data_Records.DoesNotExist:
            return HttpResponse("Data record with the provided AWBNO does not exist.")
    else:
        return HttpResponse("Only POST requests are allowed.")
