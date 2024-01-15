from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Formula

@receiver(post_migrate)
def insert_initial_data(sender, **kwargs):
    if sender.name == 'stateOfResult':
        Formula.objects.get_or_create(concept='Otros Gastos', initial_value=None)
        Formula.objects.get_or_create(concept='Otros Productos', initial_value=None)
        Formula.objects.get_or_create(concept='Gastos Financieros', initial_value=None)
        Formula.objects.get_or_create(concept='Gastos de Venta', initial_value=None)
        Formula.objects.get_or_create(concept='Gastos de Administración', initial_value=None)
        Formula.objects.get_or_create(concept='Inventario Final', initial_value=None)
        Formula.objects.get_or_create(concept='Mercadería Disponible Para la Venta', initial_value=None)
        Formula.objects.get_or_create(concept='Compras Netas', initial_value=None)
        Formula.objects.get_or_create(concept='Compras Totales', initial_value=None)
        Formula.objects.get_or_create(concept='Ventas Netas', initial_value=None)
        