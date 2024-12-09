from django import forms
from .models import Account

class accntForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'description', 'parent','account_r']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'account_r': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }