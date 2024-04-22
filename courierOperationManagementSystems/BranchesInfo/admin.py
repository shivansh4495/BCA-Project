from django.contrib import admin
from . models import Branches, PacketAssignmentDetails, delivery_Boy, delivery_Boy_ID

# Register your models here.
admin.site.register(Branches)
admin.site.register(PacketAssignmentDetails)
admin.site.register(delivery_Boy)
admin.site.register(delivery_Boy_ID)