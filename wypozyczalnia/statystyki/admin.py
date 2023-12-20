# statystyki/admin.py

from django.contrib import admin
from .models import FinansoweStatystyki

@admin.register(FinansoweStatystyki)
class FinansoweStatystykiAdmin(admin.ModelAdmin):
    list_display = ('rok', 'przychody', 'koszty', 'zysk_netto')

    def zysk_netto(self, obj):
        return obj.przychody - obj.koszty

    zysk_netto.short_description = 'Zysk netto'
