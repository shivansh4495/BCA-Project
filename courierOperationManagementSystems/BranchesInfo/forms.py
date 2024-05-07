
from django import forms
from .models import Data_Records, delivery_Boy_details

class PacketAssignmentForm(forms.Form):
    awbno = forms.ModelChoiceField(queryset=Data_Records.objects.all(), empty_label=None)
    delivery_boy = forms.ModelChoiceField(queryset=delivery_Boy_details.objects.all(), empty_label=None)
