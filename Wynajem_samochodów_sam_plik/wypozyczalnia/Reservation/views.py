from calendar import monthrange
from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from .models import Reservation, Voucher
from .serializers import ReservationSerializer, VoucherSerializer
from django.utils import timezone
from datetime import timedelta, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import FleetAvailabilitySerializer
from Car.models import Car


class ReservationList(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = Reservation.objects.all()
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')

        if year and month:
            try:
                year = int(year)
                month = int(month)
                start_date = datetime(year, month, 1).date()
                end_date = datetime(year, month, monthrange(year, month)[1]).date()
                queryset = queryset.filter(start_date__gte=start_date, end_date__lte=end_date)
            except ValueError:
                pass

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            voucher_code = serializer.validated_data.get('voucher_code', None)

            try:
                if voucher_code:
                    voucher = Voucher.objects.get(code=voucher_code)
                else:
                    voucher = None
            except Voucher.DoesNotExist:
                return Response({'error': 'Invalid voucher code'}, status=status.HTTP_400_BAD_REQUEST)


            serializer.validated_data.pop('voucher_code', None)


            serializer.validated_data['voucher'] = voucher

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser]


class FleetAvailabilityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        year = request.query_params.get('year', timezone.now().year)
        month = request.query_params.get('month', timezone.now().month)


        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({'error': 'Invalid year or month'}, status=status.HTTP_400_BAD_REQUEST)


        _, num_days = monthrange(year, month)

        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, num_days).date()

        fleet_availability = []
        current_date = start_date

        while current_date <= end_date:
            availability_status, reservations = self.check_availability(current_date)
            reserved_cars = [reservation.car for reservation in reservations]
            fleet_availability.append({
                'date': current_date,
                'available': availability_status,
                'reserved_cars': reserved_cars
            })
            current_date += timedelta(days=1)

        serializer = FleetAvailabilitySerializer(fleet_availability, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_availability(self, date):
        reservations = Reservation.objects.filter(start_date__lte=date, end_date__gte=date)
        total_cars = Car.objects.count()
        availability_status = reservations.count() < total_cars
        return availability_status, reservations


class CreateReservationView(CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            voucher_code = serializer.validated_data.get('voucher_code', None)

            try:
                if voucher_code:
                    voucher = Voucher.objects.get(code=voucher_code)
                else:
                    voucher = None
            except Voucher.DoesNotExist:
                return Response({'error': 'Invalid voucher code'}, status=status.HTTP_400_BAD_REQUEST)


            serializer.validated_data.pop('voucher_code', None)


            serializer.validated_data['voucher'] = voucher


            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CreateVoucherView(CreateAPIView):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer
    permission_classes = [IsAdminUser]

class ListVoucherView(ListAPIView):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer
    permission_classes = [IsAdminUser]