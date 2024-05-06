from django.contrib import admin
from . models import Branches, PacketAssignmentDetails, delivery_Boy_details, delivery_Boy_ID, Branch_head, Data_Records, ChargeDetails, Qr_Details

# Register your models here.
admin.site.register(Branches)
admin.site.register(PacketAssignmentDetails)
admin.site.register(delivery_Boy_details)
admin.site.register(delivery_Boy_ID)
admin.site.register(Branch_head)
admin.site.register(Data_Records)
admin.site.register(ChargeDetails)
admin.site.register(Qr_Details)