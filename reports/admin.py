from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Report

class ReportAdmin(admin.ModelAdmin):
    def Enlace_al_libro_Mayor(self, obj):
        url = reverse('major_journal')
        return format_html('<a href="{}" target="_blank">Reporte del libro mayor.</a>', url)
    def Enlace_a_balanza_de_comprobacion(self, obj):
        url = reverse('checkin_balance')
        return format_html('<a href="{}" target="_blank">Reporte de balanza de comprobación</a>', url)
    def Enalece_a_balance_general(self, obj):
        url = reverse('general_balance')
        return format_html('<a href="{}" target="_blank">Reporte de balance general</a>', url)
    
    def Enlace_a_estado_de_resultado(self, obj):
        url = reverse('general_stateOfResult_report')
        return format_html('<a href="{}" target="_blank">Reporte del estado de resultado</a>', url)
    
    def Enlace_a_catalogo_de_cuentas(self, obj):
        url = reverse('catalogue')
        return format_html('<a href="{}" target="_blank">Reporte del catalogo de cuentas</a>', url)
    
    def Enlace_a_libro_diario(self, obj):
        url = reverse('journal')
        return format_html('<a href="{}" target="_blank">Reporte del libro diario</a>', url)

    
    
    readonly_fields = ['Enlace_a_catalogo_de_cuentas','Enlace_a_libro_diario','Enlace_al_libro_Mayor','Enlace_a_balanza_de_comprobacion','Enlace_a_estado_de_resultado', 'Enalece_a_balance_general',]


    def has_change_permission(self, request, obj=None):
            # Devuelve False para desactivar la capacidad de modificar objetos
            return False
        
    def has_view_permission(self, request, obj=None):
        # Devuelve False para desactivar la capacidad de ver objetos
        return False
admin.site.register(Report, ReportAdmin)