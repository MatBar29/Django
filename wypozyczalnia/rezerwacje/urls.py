from django.urls import path
from .views import ListaSamochodowView, ListaRezerwacjiView, NowaRezerwacjaView, RezerwacjaDetailView, \
    SamochodDetailView, FleetAvailabilityAPIView

urlpatterns = [
    path('lista_samochodow/', ListaSamochodowView.as_view(), name='lista_samochodow'),
    path('lista_rezerwacji/', ListaRezerwacjiView.as_view(), name='lista_rezerwacji'),
    path('nowa_rezerwacja/', NowaRezerwacjaView.as_view(), name='nowa_rezerwacja'),
    path('rezerwacja/<int:pk>/', RezerwacjaDetailView.as_view(), name='rezerwacja-detail'),
    path('samochod/<int:pk>/', SamochodDetailView.as_view(), name='samochod-detail'),
    path('kalendarz/', FleetAvailabilityAPIView.as_view(), name='fleet_availability_api'),
    # other paths...
]
