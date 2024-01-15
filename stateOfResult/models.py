from django.db import models

# import account for catalogue
from catalogue.models import Account

class Formula(models.Model):
    """
        Representa un concepto del estado de resultado
    """
    concept=models.CharField("Concepto", max_length=250)
    initial_value= models.FloatField("Valor inicial", null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.concept} - $ { 0 if self.initial_value is None else self.initial_value}"

    class Meta:
        verbose_name="Formula"
        verbose_name_plural="Formulas"

class Term(models.Model):
    """
    representacion de un termino de la formula
    """
    account = models.ForeignKey(
        Account,
        on_delete= models.CASCADE, 
        null=False,
        blank=False,
        limit_choices_to={'parent__parent__isnull': False},#limita las cuentas que se puedan mostrar
        verbose_name="Cuenta"
    )
    operation=models.BooleanField("Operacion")
    formula = models.ForeignKey(
        Formula,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Formula" 
    )

    def __str__(self):
        return "{} {}".format("(+)" if self.operation else "(-)", self.account.name)
    

    class Meta:
        verbose_name="Termino"
        verbose_name_plural="Terminos"