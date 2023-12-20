from django.urls import path
from .views import lista_samochodow, ListaRezerwacjiView, NowaRezerwacjaView, RezerwacjaDetailView, SamochodDetailView

urlpatterns = [
    path('lista_samochodow/', lista_samochodow, name='lista_samochodow'),
    path('lista_rezerwacji/', ListaRezerwacjiView.as_view(), name='lista_rezerwacji'),
    path('nowa_rezerwacja/', NowaRezerwacjaView.as_view(), name='nowa_rezerwacja'),
    path('rezerwacja/<int:pk>/', RezerwacjaDetailView.as_view(), name='rezerwacja-detail'),
    path('samochod/<int:pk>/', SamochodDetailView.as_view(), name='samochod-detail'),
    # other paths...
]
