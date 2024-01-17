from django.db import models

class Klient(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    prawo_jazdy_numer = models.CharField(max_length=20)
    data_urodzenia = models.DateField()
    numer_telefonu = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    liczba_rezerwacji = models.IntegerField(default=0)
    aktualna_znizka = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def aktualizuj_znizke(self):
        if self.liczba_rezerwacji >= 30:
            self.aktualna_znizka = 15.0
        elif self.liczba_rezerwacji >= 20:
            self.aktualna_znizka = 10.0
        elif self.liczba_rezerwacji >= 10:
            self.aktualna_znizka = 5.0
        else:
            self.aktualna_znizka = 0.0
        self.save()


    def __str__(self):
        return f'{self.imie} {self.nazwisko} {self.email}'