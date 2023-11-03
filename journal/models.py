from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum

# import account for catalogue
from catalogue.models import Account


# Create your models here.

class Item(models.Model):
    """
    representacion de una partida del libro diario
    """
    date=models.DateTimeField("Fecha")
    value=models.CharField("Valor", max_length=250)

    def __str__(self):
        return "V/ {}".format(self.value)

    class Meta:
        verbose_name="Partida"
        verbose_name_plural="Partidas"
  
    """
    Esto es el validador que no funciona
    def clean(self):
            if self.pk:
                total_debe = self.transaction_set.filter(debit_credit=False).aggregate(Sum('balance'))['balance__sum'] or 0
                total_haber = self.transaction_set.filter(debit_credit=True).aggregate(Sum('balance'))['balance__sum'] or 0

                if total_debe != total_haber:
                    raise ValidationError("La partida no está balanceada. El total de 'Debe' y 'Haber' no coincide.")
    """


class Transaction(models.Model):
    """
    represetacion de la insersion de cuentas con su respectivo cargo
    """
    account = models.ForeignKey(
        Account,
        on_delete= models.CASCADE, #Si se borra una cuenta vale madre todo el diario
        null=False,
        blank=False,
        verbose_name="Cuenta"
    )
    balance = models.FloatField("Saldo")
    debit_credit = models.BooleanField("Tipo de saldo") #False debe | True haber
    Item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE, #En cascada porque si se borra la partida las transacciones no tienen porque estar
        null=False,
        blank=False,
        verbose_name="Partida" 
    )

    class Meta:
        verbose_name="Transacción"
        verbose_name_plural="Transacciones"
        


