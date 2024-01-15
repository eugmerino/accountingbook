from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Report

class ReportAdmin(admin.ModelAdmin):
    def link_to_major_journal(self, obj):
        url = reverse('major_journal')
        return format_html('<a href="{}" target="_blank">Reporte del libro mayor.</a>', url)
    def link_to_checking_balance(self, obj):
        url = reverse('checkin_balance')
        return format_html('<a href="{}" target="_blank">Reporte del libro mayor.</a>', url)
    
    def link_to_report_state_of_result(self, obj):
        url = reverse('general_stateOfResult_report')
        return format_html('<a href="{}" target="_blank">Reporte del estado de resultado.</a>', url)

    readonly_fields = ['link_to_major_journal','link_to_checking_balance', 'link_to_report_state_of_result',]

admin.site.register(Report, ReportAdmin)