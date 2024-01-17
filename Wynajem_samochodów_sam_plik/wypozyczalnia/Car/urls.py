from django.urls import path
from .views import ListCarView, CarDetailView

urlpatterns = [
    path('lista_samochodow/', ListCarView.as_view(), name='lista_samochodow'),
    path('samochod/<int:pk>/', CarDetailView.as_view(), name='samochod-detail'),
]