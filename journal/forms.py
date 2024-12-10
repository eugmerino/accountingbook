from django import forms
from django.forms import inlineformset_factory
from .models import Item, Transaction
from django.forms import BaseInlineFormSet, ValidationError

# Formulario de las partidas
class itemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['date', 'value', 'isItemEnd']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'isItemEnd': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }




class TransactionFormSetBase(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_debit = 0
        total_credit = 0

        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False): 
                balance = form.cleaned_data.get('balance', 0)
                debit_credit = form.cleaned_data.get('debit_credit', False)

                if debit_credit:  # True significa "Haber"
                    total_credit += balance
                else:  # False significa "Debe"
                    total_debit += balance

        if total_debit != total_credit:
            raise ValidationError("Las transacciones no están balanceadas: el total de Débito debe ser igual al total de Crédito.")

# Formset para transacciones
TransactionFormSet = inlineformset_factory(
    Item,
    Transaction,
    fields=['account', 'balance', 'debit_credit'],
    widgets={
        'account': forms.Select(attrs={'class': 'form-select'}),
        'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        'debit_credit': forms.Select(
            choices=[(False, 'Débito'), (True, 'Crédito')],
            attrs={'class': 'form-select'}
        ),
    },
    formset=TransactionFormSetBase,  # Asigna la clase personalizada
    extra=2,
    can_delete=True
)
