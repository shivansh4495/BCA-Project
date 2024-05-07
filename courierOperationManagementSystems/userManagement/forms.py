from django import forms
from captcha.fields import CaptchaField
from .models import Client
from homeapp.models import Feedback
from datetime import datetime

class MyForm(forms.Form):
    captcha = CaptchaField()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['Client_Address', 'Client_contact_No']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['Fname', 'Lname', 'ContactNo', 'Branch_name', 'FeedbackMsg', 'Email']
        labels = {
            'Fname': 'First Name',
            'Lname': 'Last Name',
            'ContactNo': 'Your Contact Number',
            'Branch_Id': 'Branch ID',
            'Branch_name': 'Enter Branch Name',
            'FeedbackMsg': 'Enter Your Queries',
            'Email': 'Enter Your Email Address',
        }

    def save(self, commit=True):
        feedback = super().save(commit=False)
        feedback.Date = datetime.now()
        if commit:
            feedback.save()
        return feedback
