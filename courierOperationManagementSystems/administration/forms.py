from django import forms
from BranchesInfo.models import Branches

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branches
        fields = '__all__'
