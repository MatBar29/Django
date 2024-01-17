import datetime
from decimal import Decimal
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from Car.models import Car
from Client.models import Klient

class Voucher(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    is_percentage = models.BooleanField(default=False)

    def is_valid(self):
        return datetime.date.today() <= self.expiration_date

    def __str__(self):
        return f'{self.code} - Discount: {"%" if self.is_percentage else "zł"}{self.discount_amount}'


class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    imie = models.CharField(max_length=50, null=True, blank=True)
    nazwisko = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True)


    def clean(self):

        current_date = timezone.now().date()

        if self.start_date < current_date:
            raise ValidationError("Data rozpoczęcia rezerwacji nie może być w przeszłości.")

        if self.end_date < current_date:
            raise ValidationError("Data zakończenia rezerwacji nie może być w przeszłości.")

        if self.start_date > self.end_date:
            raise ValidationError("Data zakończenia rezerwacji nie może być wcześniejsza niż data rozpoczęcia.")

        overlapping_reservations = Reservation.objects.filter(
            car=self.car,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date
        ).exclude(id=self.id)

        if overlapping_reservations.exists():
            raise ValidationError("Ten samochód jest już zarezerwowany w wybranym terminie.")

        super().clean()


    def save(self, *args, **kwargs):
        self.clean()
        duration = (self.end_date - self.start_date).days
        base_price = duration * Decimal(self.car.cena_wynajmu) + Decimal(self.car.cena_wynajmu)

        if self.voucher and self.voucher.is_valid():
            if self.voucher.is_percentage:
                discount = base_price * Decimal(self.voucher.discount_amount) / Decimal(100)
                self.total_price = base_price - discount
            else:
                self.total_price = base_price - Decimal(self.voucher.discount_amount)
        else:
            self.total_price = base_price

        klient = Klient.objects.get(email=self.email) if self.email else None

        if klient:
            klient.liczba_rezerwacji += 1
            klient.aktualizuj_znizke()

            if klient.aktualna_znizka > 0:
                klient_znizka_decimal = Decimal(klient.aktualna_znizka)
                discount = self.total_price * (klient_znizka_decimal / Decimal(100))
                self.total_price -= discount

        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.car} reserved by {self.client} from {self.start_date} to {self.end_date}'

