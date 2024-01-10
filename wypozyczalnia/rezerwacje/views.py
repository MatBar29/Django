from datetime import timedelta

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from .models import Samochod, Rezerwacja
from .serializers import SamochodSerializer, RezerwacjaSerializer, FleetAvailabilitySerializer


class ListaSamochodowView(generics.ListCreateAPIView):
    serializer_class = SamochodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Samochod.objects.filter(dostepny=True)

        # Filtrowanie według marki
        marka = self.request.query_params.get('marka', None)
        if marka:
            queryset = queryset.filter(marka__icontains=marka)

        # Filtrowanie według modelu
        model = self.request.query_params.get('model', None)
        if model:
            queryset = queryset.filter(model__icontains=model)

        # Filtrowanie według roku produkcji
        rok_produkcji = self.request.query_params.get('rok_produkcji', None)
        if rok_produkcji:
            queryset = queryset.filter(rok_produkcji=rok_produkcji)

        return queryset

class ListaRezerwacjiView(generics.ListCreateAPIView):
    queryset = Rezerwacja.objects.all()
    serializer_class = RezerwacjaSerializer
    permission_classes = [IsAuthenticated]


class NowaRezerwacjaView(generics.CreateAPIView):
    serializer_class = RezerwacjaSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        samochod_id = data.get('samochod')
        data_wypozyczenia = data.get('data_wypozyczenia')
        data_zwrotu = data.get('data_zwrotu')

        # Sprawdź dostępność samochodu w podanym przedziale dat
        if self.is_car_available(samochod_id, data_wypozyczenia, data_zwrotu):
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': 'Selected car is not available for the specified dates.'}, status=status.HTTP_400_BAD_REQUEST)

    def is_car_available(self, samochod_id, data_wypozyczenia, data_zwrotu):
        # Sprawdź, czy dla danego samochodu nie ma już rezerwacji na dane dni
        existing_reservations = Rezerwacja.objects.filter(
            samochod_id=samochod_id,
            data_wypozyczenia__lte=data_zwrotu,
            data_zwrotu__gte=data_wypozyczenia
        )

        return not existing_reservations.exists()

class RezerwacjaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rezerwacja.objects.all()
    serializer_class = RezerwacjaSerializer
    permission_classes = [IsAuthenticated]

class SamochodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Samochod.objects.filter(dostepny=True)
    serializer_class = SamochodSerializer
    permission_classes = [IsAuthenticated]

class SamochodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Samochod.objects.filter(dostepny=True)
    serializer_class = SamochodSerializer
    permission_classes = [IsAuthenticated]

class FleetAvailabilityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        end_date = today + timedelta(days=30)  # You can adjust the number of days as needed

        fleet_availability = []

        while today <= end_date:
            availability_status, reserved_cars = self.check_availability(today)
            fleet_availability.append({'date': today, 'available': availability_status, 'reserved_cars': reserved_cars})
            today += timedelta(days=1)

        serializer = FleetAvailabilitySerializer(fleet_availability, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_availability(self, date):
        # Check if there are any reservations for the given date
        reservations = Rezerwacja.objects.filter(data_wypozyczenia__lte=date, data_zwrotu__gte=date)
        reserved_cars = reservations.values('samochod__id', 'samochod__marka', 'samochod__model').distinct()

        # Get the total number of cars
        total_cars = Samochod.objects.count()

        # If all cars are reserved for the given date, the fleet is not available
        availability_status = len(reserved_cars) < total_cars

        return availability_status, reserved_cars
