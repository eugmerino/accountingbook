# Generated by Django 4.2.5 on 2023-09-28 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_alter_account_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='code',
            field=models.CharField(help_text='El código se autogenera al guardar la cuenta', max_length=50, verbose_name='Código'),
        ),
    ]
