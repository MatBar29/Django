from django.contrib import admin
from .models import Samochod, Klient, Rezerwacja

@admin.register(Samochod)
class SamochodAdmin(admin.ModelAdmin):
    list_display = ('marka', 'model', 'rok_produkcji', 'dostepny')
    list_filter = ('dostepny',)
    search_fields = ('marka', 'model')

@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):
    list_display = ('imie', 'nazwisko', 'email')
    search_fields = ('imie', 'nazwisko', 'email')

@admin.register(Rezerwacja)
class RezerwacjaAdmin(admin.ModelAdmin):
    list_display = ('samochod', 'klient', 'data_wypozyczenia', 'data_zwrotu')
    list_filter = ('data_wypozyczenia', 'data_zwrotu')
    search_fields = ('samochod__marka', 'klient__nazwisko', 'klient__email')

