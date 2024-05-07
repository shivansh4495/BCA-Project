from django import forms
from captcha.fields import CaptchaField
from .models import Client


class MyForm(forms.Form):
    captcha = CaptchaField()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['Client_Address', 'Client_contact_No']