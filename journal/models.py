from django.db import models
from django.core.exceptions import ValidationError


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
    
    
class Transaction(models.Model):
    """
    represetacion de la insersion de cuentas con su respectivo cargo
    """
    account = models.ForeignKey(
        Account,
        on_delete= models.CASCADE, 
        null=False,
        blank=False,
        limit_choices_to={'parent__parent__isnull': False},#limita las cuentas que se puedan mostrar
        verbose_name="Cuenta"
    )
    balance = models.FloatField("Saldo")
    debit_credit = models.BooleanField("Debe/Haber") #False debe | True haber
    Item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Partida" 
    )

    def __str__(self):
        return "{} - $ {}".format(self.account,self.balance)

    class Meta:
        verbose_name="Transacción"
        verbose_name_plural="Transacciones"
        


