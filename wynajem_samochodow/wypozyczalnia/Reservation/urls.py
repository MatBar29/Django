from django.urls import path
from .views import ReservationList, ReservationDetail, FleetAvailabilityAPIView, CreateVoucherView, ListVoucherView, \
    CreateReservationView

urlpatterns = [
    path('reservations/', ReservationList.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/', ReservationDetail.as_view(), name='reservation-detail'),
    path('kalendarz/', FleetAvailabilityAPIView.as_view(), name='fleet_availability_api'),
    path('create-voucher/', CreateVoucherView.as_view(), name='create-voucher'),
    path('vouchers/', ListVoucherView.as_view(), name='list-vouchers'),
    path('create-reservation/', CreateReservationView.as_view(), name='create-reservation'),
]
