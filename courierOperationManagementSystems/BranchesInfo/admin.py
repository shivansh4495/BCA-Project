from django.contrib import admin
from . models import Branches, PacketAssignmentDetails, delivery_Boy_details, delivery_Boy_ID, Branch_head

# Register your models here.
admin.site.register(Branches)
admin.site.register(PacketAssignmentDetails)
admin.site.register(delivery_Boy_details)
admin.site.register(delivery_Boy_ID)
admin.site.register(Branch_head)