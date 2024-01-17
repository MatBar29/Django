from django.urls import path
from .views import TotalReservationsSumView, MonthComparisonView

urlpatterns = [
    path('total-sum/', TotalReservationsSumView.as_view(), name='total_reservations_sum'),
    path('compare-months/', MonthComparisonView.as_view(), name='compare-months'),
]
