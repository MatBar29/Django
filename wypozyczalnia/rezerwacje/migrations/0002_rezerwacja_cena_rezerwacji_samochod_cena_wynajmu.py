# Generated by Django 4.2.8 on 2023-12-20 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rezerwacje', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rezerwacja',
            name='cena_rezerwacji',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='samochod',
            name='cena_wynajmu',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
