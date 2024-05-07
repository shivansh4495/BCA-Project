
from django import forms
from BranchesInfo.models import Branches, ChargeDetails, Branch_head

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branches
        fields = '__all__'


class ChargeDetailsForm(forms.ModelForm):
    class Meta:
        model = ChargeDetails
        fields = '__all__'
        labels = {
            'PlanCode': 'Plan Code',
            'Description': 'Description',
            'Weight': 'Weight',
            'Amount': 'Amount',
        }


class BranchHeadForm(forms.ModelForm):
    class Meta:
        model = Branch_head
        fields = '__all__'
        labels = {
            'Branch_head_Name': 'Name',
            'Branch_head_Username': 'Branch Head UserName',
            'Branch_head_Password': 'Password',
            'Branch_CD': 'Branch CD',
            'User_Type': 'User Type',
        }