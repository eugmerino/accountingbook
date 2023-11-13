from django.db import models
from django.db.models.query import QuerySet

# import signals (Disparadores)
from django.dispatch import receiver
from django.db.models.signals import pre_save

class MainAccountsManager(models.Manager):
    """
        Este manager retorna las cuentas principales
    """
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(parent=None)


class Account(models.Model):
    """
    representa una cuenta de catalogo
    """
    code=models.CharField(
        "Código", max_length=50,
        help_text="El código se autogenera al guardar la cuenta",
        unique=True
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
        return "{} - {}".format(self.code, self.name)
    
    def is_parent(self):
        """
        Evalua si la cuenta tiene cuentas hijos
        """
        if Account.objects.filter(parent=self.id).count() > 0:
            return True
        return False
    
    objects = models.Manager()
    mainAccounts_objects = MainAccountsManager()

    class Meta:
         verbose_name="Cuenta"
         verbose_name_plural="Cuentas"

def account_exists(code):
    """
    Verifica si existe el codigo
    """
    if Account.filter(pk=code).exists():
        return True
    return False

def generate_code(account_id=None, parent=False, code=""):
    """
    Genera el código para la cuenta a crear
    """
    new_code = ''
    if not parent:
        last_code = Account.objects.filter(parent=None).last()
        if last_code:
            new_code = str(int(last_code.code) + 1)
        else:
            new_code = code + '1'
    else:
        last_code = Account.objects.filter(parent=account_id).last()
        if last_code:
            new_code = str(int(last_code.code) + 1)
        else:
            if len(code)>1:
                new_code = code + '01'
            else:
                new_code = code + '1'
    return new_code
            
# Signals
@receiver(pre_save, sender=Account)
def account_pre_save_receiver(sender, instance, *args, **kwargs):
    """
    Se encarga de asignar el código de la cuenta.
    Se ejecuta antes de guardar la cuenta.
    """
    if not instance.id:
        if not instance.parent:
            instance.code=generate_code(None, False)
        else:
            instance.code=generate_code(instance.parent_id, True, instance.parent.code)    
            
                   
class Balance_type(models.Model):
    """"
    Representa la asignacion del tipo de saldo a las cuentas
    principales en el catalogo de cuentas
    """
    main_account=models.OneToOneField(
        'Account',
        on_delete=models.CASCADE,
        limit_choices_to={'parent': None},
        verbose_name="Cuenta principal"
    )
    nature_of_balance = models.BooleanField(
        default=False
    )

    def __str__(self):
        return "{} - {}".format(self.main_account, get_nature_of_balance(self.nature_of_balance))
   
    class Meta:
     verbose_name="Naturaleza del Saldo"
     verbose_name_plural="Naturaleza de los Saldos"

def get_nature_of_balance(nature_of_balance):
        return 'Acreedor' if nature_of_balance else 'Deudor'
        