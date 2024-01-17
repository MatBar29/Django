import calendar
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TotalSumSerializer
from Reservation.models import Reservation
from django.db.models import Sum, Count, Avg, F
from Car.models import Car
from rest_framework.permissions import IsAdminUser


class TotalReservationsSumView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, *args, **kwargs):
        year = request.query_params.get('year', timezone.now().year)
        month = request.query_params.get('month', timezone.now().month)
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({"error": "Invalid year or month"}, status=400)

        def get_month_data(year, month):
            _, last_day = calendar.monthrange(year, month)
            reservations = Reservation.objects.filter(
                start_date__gte=timezone.datetime(year, month, 1),
                end_date__lte=timezone.datetime(year, month, last_day)
            ).select_related('car')

            total_sum = reservations.aggregate(Sum('total_price'))['total_price__sum'] or 0
            count_reservations = reservations.count()
            average_price = round(reservations.aggregate(Avg('total_price'))['total_price__avg'] or 0, 2)

            most_common_model_query = reservations.values('car__model').annotate(count=Count('car__model')).order_by(
                '-count').first()
            most_common_brand_query = reservations.values('car__marka').annotate(count=Count('car__marka')).order_by(
                '-count').first()

            most_common_model = most_common_model_query['car__model'] if most_common_model_query else None
            most_common_brand = most_common_brand_query['car__marka'] if most_common_brand_query else None

            average_duration = \
            reservations.annotate(duration=F('end_date') - F('start_date')).aggregate(avg_duration=Avg('duration'))[
                'avg_duration']
            average_duration_days = average_duration.days if average_duration else 0

            return {
                'total_sum': total_sum,
                'count_reservations': count_reservations,
                'average_price': average_price,
                'most_common_model': most_common_model,
                'most_common_brand': most_common_brand,
                'average_duration_days': average_duration_days
            }

        data = get_month_data(year, month)

        serializer = TotalSumSerializer(data=data)
        if serializer.is_valid():
                return Response(serializer.data)
        else:
             return Response(serializer.errors, status=400)


class MonthComparisonView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, *args, **kwargs):
        year1 = request.query_params.get('year1', timezone.now().year)
        month1 = request.query_params.get('month1', timezone.now().month)

        year2 = request.query_params.get('year2', timezone.now().year)
        month2 = request.query_params.get('month2', timezone.now().month)

        try:
            year1, month1, year2, month2 = map(int, [year1, month1, year2, month2])
        except ValueError:
            return Response({"error": "Invalid year or month"}, status=400)


        def get_month_data(year, month):
            _, last_day = calendar.monthrange(year, month)
            reservations = Reservation.objects.filter(
                start_date__gte=timezone.datetime(year, month, 1),
                end_date__lte=timezone.datetime(year, month, last_day)
            ).select_related('car')

            total_sum = reservations.aggregate(Sum('total_price'))['total_price__sum'] or 0
            count_reservations = reservations.count()
            average_price = round(reservations.aggregate(Avg('total_price'))['total_price__avg'] or 0, 2)

            most_common_model_query = reservations.values('car__model').annotate(count=Count('car__model')).order_by(
                '-count').first()
            most_common_brand_query = reservations.values('car__marka').annotate(count=Count('car__marka')).order_by(
                '-count').first()

            most_common_model = most_common_model_query['car__model'] if most_common_model_query else None
            most_common_brand = most_common_brand_query['car__marka'] if most_common_brand_query else None

            average_duration = \
            reservations.annotate(duration=F('end_date') - F('start_date')).aggregate(avg_duration=Avg('duration'))[
                'avg_duration']
            average_duration_days = average_duration.days if average_duration else 0

            return {
                'total_sum': total_sum,
                'count_reservations': count_reservations,
                'average_price': average_price,
                'most_common_model': most_common_model,
                'most_common_brand': most_common_brand,
                'average_duration_days': average_duration_days
            }

        data1 = get_month_data(year1, month1)
        data2 = get_month_data(year2, month2)


        return Response({
            'Porównywany': data1,
            'Do którego jest porównywany': data2,
            'Porównanie': {
                'total_sum_difference (zł)': data1['total_sum'] - data2['total_sum'],
                'count_reservations_difference': data1['count_reservations'] - data2['count_reservations'],
                'average_price (zł)': data1['average_price'] - data2['average_price'],
                'average_duration_days': data1['average_duration_days'] - data2['average_duration_days'],
            }
        })

