# statystyki/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from rezerwacje.models import Rezerwacja
from statystyki.models import FinansoweStatystyki

@receiver(post_save, sender=Rezerwacja)
def update_financial_statistics(sender, instance, **kwargs):
    if instance.data_wypozyczenia.year == instance.data_zwrotu.year:
        statystyki, created = FinansoweStatystyki.objects.get_or_create(rok=instance.data_wypozyczenia.year)
        statystyki.przychody = FinansoweStatystyki.objects.filter(rok=instance.data_wypozyczenia.year).aggregate(models.Sum('cena_rezerwacji'))['cena_rezerwacji__sum']
        statystyki.save()
