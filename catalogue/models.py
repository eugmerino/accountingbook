from django.db import models


class Account(models.Model):
    """
    representa una cuenta de catalogo
    """
    code=models.CharField("Código", max_length=50)
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