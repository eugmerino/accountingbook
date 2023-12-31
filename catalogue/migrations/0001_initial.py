# Generated by Django 4.2.5 on 2023-09-26 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='Código')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('description', models.TextField(max_length=250, verbose_name='Descripción')),
                ('account_r', models.BooleanField(default=False, help_text='Activar si es cuenta complementaria', verbose_name='Cuenta R')),
            ],
            options={
                'verbose_name': 'Cuenta',
                'verbose_name_plural': 'Cuentas',
            },
        ),
    ]
