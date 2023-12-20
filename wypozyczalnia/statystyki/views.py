# Przykładowa logika w widoku

from django.shortcuts import render
from .models import FinansoweStatystyki

def przykladowy_widok(request):
    # ... Twoja logika związana z transakcjami finansowymi

    # Przykładowe uaktualnienie statystyk
    rok = 2023  # Możesz dostosować rok według potrzeb
    przychody = 10000  # Przykładowa wartość przychodów
    koszty = 5000  # Przykładowa wartość kosztów

    statystyki, created = FinansoweStatystyki.objects.get_or_create(rok=rok)
    statystyki.przychody += przychody
    statystyki.koszty += koszty
    statystyki.save()

    return render(request, 'przykladowy_szablon.html')
