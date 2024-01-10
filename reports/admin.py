from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Report

class ReportAdmin(admin.ModelAdmin):
    def link_to_report(self, obj):
        url = reverse('general_ledger_report')
        return format_html('<a href="{}" target="_blank">Reporte del libro mayor.</a>', url)

    readonly_fields = ['link_to_report']

admin.site.register(Report, ReportAdmin)