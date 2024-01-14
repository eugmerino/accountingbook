from django.contrib import admin
from django import forms
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver

from catalogue.models import Account
from journal.models import Item,Transaction

class TransactionAdminForm(forms.ModelForm):
    """
    Forms de las transacciones por partidas
    """
    class Meta:
        model = Transaction

        fields = (
            'account',
            'balance',
            'debit_credit'
        )
        widgets = {
            'debit_credit': forms.RadioSelect(choices=((False, 'Debe'), (True, 'Haber')))
        }

    
class TransactionInlineFormSet(forms.BaseInlineFormSet):
    """
    Valida que hayan igual cantidad de transacciones marcadas con debe y con haber
    """
    def clean(self):
        total_debit = 0
        total_credit = 0

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                balance = form.cleaned_data.get('balance',0)
                debit_credit = form.cleaned_data.get('debit_credit', False)
                if debit_credit:
                    total_credit +=balance
                else:
                    total_debit += balance

        if total_debit != total_credit:
            raise forms.ValidationError("La partida no esta balanceada.")


class registreTransactionInLine(admin.TabularInline):
    """
    carga las transacciones dentro de la creacion de partidas
    """
    model = Transaction
    form = TransactionAdminForm
    autocomplete_fields = ('account',)
    formset = TransactionInlineFormSet
    extra = 0
    

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Carga el listado de las partidas
    """
    list_display_links = ['date']
    list_display = (
        'get_item_number',
        'date',
        'get_item_transaction_total',
        'value',
        'isItemEnd'
        )
    ordering = ['date']
    """
    Caga el agregar/modificar partida
    """
    fields = (
        ('date'),
        'value',
        'isItemEnd'
    )
    inlines = [registreTransactionInLine]

    def get_item_number(self, obj):
        """
        Coloca un numero correlativo a la partida
        """
        all_items = Item.objects.all().order_by('date')
        item_list = list(all_items)
        index = item_list.index(obj) + 1
        return index
    get_item_number.short_description = 'Número de partida'
        
    def get_item_transaction_total(self, obj):
        """
        Devuelve el saldo total de la transaccion
        """
        saldo = obj.transaction_set.filter(debit_credit=False).aggregate(Sum('balance'))['balance__sum'] or 0
        return saldo
    get_item_transaction_total.short_description = 'Saldo'

