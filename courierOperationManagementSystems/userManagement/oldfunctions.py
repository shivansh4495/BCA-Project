def generate_and_store_qr(request):
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
            
            # Check if a QR code with the same AWBNO already exists
            existing_qr = Qr_Details.objects.filter(awbno=awbno)
            if existing_qr.exists():
                # If a QR code with the same AWBNO exists, delete it
                existing_qr.delete()

            # Save the QR code image to the static folder
            static_folder = settings.STATIC_ROOT
            file_path = os.path.join(static_folder, f'qrcode_{awbno}.png')
            with open(file_path, 'wb') as f:
                f.write(buffer.getvalue())

            # Create Qr_Details object
            qr_detail = Qr_Details.objects.create(awbno=awbno, Qr_image=file_path)
            qr_detail.save()
            
            # Update qr_images dictionary with the URL of the generated QR code image
            # qr_images[awbno] = f"/static/barcode_{awbno}.png"  
            messages.success(request, "Barcode generated and stored successfully.")
        except Data_Records.DoesNotExist:
            messages.error(request, "Data record with the provided AWBNO does not exist.")
    else:
        messages.error(request, "Only POST requests are allowed.")
    
    return redirect('BranchesInfo:delivery_boy_dashboard')  # Redirect to a specific view after processing
