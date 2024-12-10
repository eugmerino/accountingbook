from django import forms
from .models import Account
from .models import Balance_type

class accntForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'description', 'parent','account_r']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'parent': forms.Select(attrs={'class': 'form-select mb-3'}),
            'account_r': forms.CheckboxInput(attrs={'class': 'form-check-input mb-3'}),

        }

class natureForm(forms.ModelForm):
    class Meta:
        model = Balance_type
        fields = ['main_account', 'nature_of_balance']
        widgets = {
            'main_account': forms.Select(attrs={'class': 'form-select mb-3'}),
            'nature_of_balance': forms.Select(
            choices=[(False, 'Deudor'), (True, 'Acreedor')],
            attrs={'class': 'form-select'}
        ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excluir las cuentas ya presentes en Balance_type
        assigned_accounts = Balance_type.objects.values_list('main_account', flat=True)
        self.fields['main_account'].queryset = Account.objects.filter(
            parent=None
        ).exclude(id__in=assigned_accounts)