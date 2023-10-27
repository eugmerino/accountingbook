from django.contrib import admin
from django.urls import include, path

from catalogue.models import Account


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