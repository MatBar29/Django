from django.db import models


class Car(models.Model):
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    rok_produkcji = models.IntegerField()
    dostepny = models.BooleanField(default=True)
    cena_wynajmu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rodzaj_paliwa = models.CharField(max_length=20, null=True, blank=True)
    pojemnosc_silnika = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f'{self.marka} {self.model} ({self.cena_wynajmu}zł/dzień)'