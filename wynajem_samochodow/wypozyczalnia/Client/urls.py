from django.urls import path
from .views import (
    KlientListView,
    KlientCreateView,
    KlientRetrieveView,
    KlientUpdateView,
    KlientDeleteView
)

urlpatterns = [
    path('klients/', KlientListView.as_view(), name='klient-list'),
    path('klients/create/', KlientCreateView.as_view(), name='klient-create'),
    path('klients/<int:pk>/', KlientRetrieveView.as_view(), name='klient-detail'),
    path('klients/<int:pk>/update/', KlientUpdateView.as_view(), name='klient-update'),
    path('klients/<int:pk>/delete/', KlientDeleteView.as_view(), name='klient-delete'),]
