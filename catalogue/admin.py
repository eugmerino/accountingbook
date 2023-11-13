from typing import Any
from django.contrib import admin
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey
from django.forms.fields import TypedChoiceField
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from django.urls import include, path
from django import forms

from catalogue.models import Account, Balance_type

#-------- Admin site --------
admin.site.index_title = "Accounting Book"
admin.site.site_header = "Accounting Book"
admin.site.site_title = "Accounting Book"
# ---------------------------

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'description',
        'account_r',
    )
    list_display_links = ['name']
    fields = (
        'code',
        'name',
        'description',
        'parent',
        'account_r',
    )
    search_fields = ('name', 'code')
    autocomplete_fields = ('parent',)
    list_per_page = 10
    ordering = ['code']

    def get_readonly_fields(self, request, obj=None):
        """
        Retorna los campos de la cuenta que no se podrán editar
        """
        hidden_fields = []
        if obj:
            hidden_fields.append('parent')
            if obj.is_parent():
                hidden_fields.append('code')
        else:
            hidden_fields.append('code')
        return hidden_fields  
    

class BalanceTypeAdminForm(forms.ModelForm):
    class Meta:
        model = Balance_type
        fields = '__all__'
    nature_of_balance = forms.ChoiceField(
        choices=[(True, 'Acreedor'), (False, 'Deudor')],
        widget=forms.RadioSelect,
        label="Naturaleza del saldo"
    )


@admin.register(Balance_type)
class BalanceTypeAdmin(admin.ModelAdmin):
    list_display = (
        'main_account',
        'get_nature_of_balance',
    )
    fields = (
        ('main_account', 'nature_of_balance'),
    )
    list_display_links = ['main_account']
    list_per_page = 10
    autocomplete_fields=['main_account']
    ordering = ['main_account']
    form = BalanceTypeAdminForm 

    def get_nature_of_balance(self, obj):
        return 'Acreedor' if obj.nature_of_balance else 'Deudor'
    get_nature_of_balance.short_description = 'Naturaleza del saldo'


        
        