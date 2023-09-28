from django.db import models

# import signals (Disparadores)
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Account(models.Model):
    """
    representa una cuenta de catalogo
    """
    code=models.CharField(
        "Código", max_length=50,
        help_text="El código se autogenera al guardar la cuenta"
    )
    name=models.CharField("Nombre", max_length=200)
    description = models.TextField("Descripción", max_length=250)
    parent=models.ForeignKey('self',
        on_delete = models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Cuenta padre"
    )
    account_r = models.BooleanField(
        "Cuenta R",
        help_text="Activar si es cuenta complementaria",
        default=False
    )

    def __str__(self):
        return self.name
    
    class Meta:
         verbose_name="Cuenta"
         verbose_name_plural="Cuentas"

def generate_code(account_id=None, parent=False, code=""):
    """
    Genera el código para la cuenta a crear
    """
    last_id = Account.objects.filter(parent=account_id).count() + 1
    return code + str(last_id)

# Signals
@receiver(pre_save, sender=Account)
def account_pre_save_receiver(sender, instance, *args, **kwargs):
    """
    Se encarga de asignar el código de la cuenta.
    Se ejecuta antes de guardar la cuenta.
    """
    if not instance.id:
        if not instance.parent:
            instance.code=generate_code(None, True)
        else:
            instance.code=generate_code(instance.parent_id, False, instance.parent.code)
            