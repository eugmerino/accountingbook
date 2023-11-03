from django.contrib import admin
from django import forms
from django.db.models import Sum
from django.core.exceptions import ValidationError


from journal.models import Item,Transaction

#-------- Admin site --------
admin.site.index_title = "Accounting Book"
admin.site.site_header = "Accounting Book"
admin.site.site_title = "Accounting Book"
# ---------------------------

    
class TransactionAdminForm(forms.ModelForm):
    """
    cambia el formato del boolean por radiobuttons
    """
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'debit_credit': forms.RadioSelect(choices=((False, 'Debe'), (True, 'Haber')))
        }


class registreTransactionInLine(admin.TabularInline):
    """
    carga la transaccion de registros dentro de la creacion de partidas
    """
    model = Transaction
    form = TransactionAdminForm
    extra = 0


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    cargado de partidas
    """
    inlines = [registreTransactionInLine]
    list_display = (
        'get_item_number',
        'date',
        'get_item_transaction_total',
        'value'
        )
    
    

    list_display_links = ['date']
    fields = (
        'date',
        'value'
    )


    ordering = ['date']

    
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
        saldo = obj.transaction_set.filter(debit_credit=False).aggregate(Sum('balance'))['balance__sum'] or 0
        return saldo
    get_item_transaction_total.short_description = 'Saldo'

    def is_balanced(self, obj):
        total_debe = obj.transaction_set.filter(debit_credit=False).aggregate(Sum('balance'))['balance__sum'] or 0
        total_haber = obj.transaction_set.filter(debit_credit=True).aggregate(Sum('balance'))['balance__sum'] or 0

        if total_debe != total_haber:
            raise ValidationError("La partida no está balanceada. El total de 'Debe' y 'Haber' no coincide.")
