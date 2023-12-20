# rezerwacje/forms.py

from django import forms
from .models import Rezerwacja

class RezerwacjaForm(forms.ModelForm):
    class Meta:
        model = Rezerwacja
        fields = ['samochod', 'klient', 'data_wypozyczenia', 'data_zwrotu']

    def clean(self):
        cleaned_data = super().clean()
        samochod = cleaned_data.get('samochod')
        data_wypozyczenia = cleaned_data.get('data_wypozyczenia')
        data_zwrotu = cleaned_data.get('data_zwrotu')

        if samochod and data_wypozyczenia and data_zwrotu:
            delta = data_zwrotu - data_wypozyczenia
            cena_wynajmu = samochod.cena_wynajmu * delta.days
            cleaned_data['cena_rezerwacji'] = cena_wynajmu
