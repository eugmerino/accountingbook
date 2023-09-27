from django.contrib import admin
from catalogue.models import Account


#-------- Admin site --------
admin.site.index_title = "Accounting Book"
admin.site.site_header = "Administración"
admin.site.site_title = "Accounting Book"
# ---------------------------

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'account_r',
    )
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
    readonly_fields = ('code',)