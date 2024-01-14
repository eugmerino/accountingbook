from django.contrib import admin
from django import forms
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver

from catalogue.models import Account
from stateOfResult.models import Formula, Term

class TermAdminForm(forms.ModelForm):
    """
    Forms de los terminos por formula
    """
    class Meta:
        model = Term

        fields = (
            'account',
            'operation',
        )
        widgets = {
            'operation': forms.RadioSelect(choices=((False, '-'), (True, '+')))
        }


class registreTermInLine(admin.TabularInline):
    """
    carga las transacciones dentro de la creacion de partidas
    """
    model = Term
    form = TermAdminForm
    autocomplete_fields = ('account',)
    extra = 0


class FormulaForm(forms.ModelForm):
    class Meta:
        model = Formula
        fields = ['concept', 'initial_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['initial_value'].widget = forms.TextInput(attrs={'placeholder': '$'})


@admin.register(Formula)
class FormulaAdmin(admin.ModelAdmin):
    """
    Carga el listado de las Formulas
    """
    form = FormulaForm
    list_display_links = ['concept']
    list_display = (
        'concept',
        'formatted_initial_value',
        )
    readonly_fields = ('concept',)
    fields = (
        ('initial_value'),
    )

    def formatted_initial_value(self, obj):
        if obj.initial_value is None:
            return f"$ 0"
        else:
            return f"$ {obj.initial_value}"
    formatted_initial_value.short_description = 'Valor inicial'

    def has_add_permission(self, request):
        # Devuelve False para desactivar la capacidad de agregar nuevos objetos
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Devuelve False para desactivar la capacidad de eliminar objetos
        return False

    inlines = [registreTermInLine]