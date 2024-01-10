# rezerwacje/models.py

from django.db import models


class Samochod(models.Model):
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    rok_produkcji = models.IntegerField()
    dostepny = models.BooleanField(default=True)
    cena_wynajmu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rodzaj_paliwa = models.CharField(max_length=20, null=True, blank=True)
    pojemnosc_silnika = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f'{self.marka} {self.model}'

class Klient(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'

class Rezerwacja(models.Model):
    samochod = models.ForeignKey(Samochod, on_delete=models.CASCADE)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    data_wypozyczenia = models.DateField()
    data_zwrotu = models.DateField()
    cena_rezerwacji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.samochod and self.data_wypozyczenia and self.data_zwrotu:
            delta = self.data_zwrotu - self.data_wypozyczenia
            cena_wynajmu = self.samochod.cena_wynajmu
            self.cena_rezerwacji = cena_wynajmu * delta.days
        super().save(*args, **kwargs)
