from rest_framework import serializers
from .models import Reservation, Voucher
from Car.models import Car
from django.utils import timezone
from Client.models import Klient


class ReservationSerializer(serializers.ModelSerializer):
    voucher_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    class Meta:
        model = Reservation
        fields = ['id','car', 'imie', 'nazwisko', 'email', 'start_date', 'end_date', 'voucher_code', 'total_price']

    def create(self, validated_data):
        klient_data = validated_data.pop('klient', None)

        reservation = Reservation.objects.create(**validated_data)

        if klient_data:
            pass

        return reservation

    def validate(self, data):
        car = data.get('car')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        current_date = timezone.now().date()
        imie = data.get('imie')
        nazwisko = data.get('nazwisko')
        email = data.get('email')

        if not imie or not nazwisko or not email:
            raise serializers.ValidationError({"error": "Imię, nazwisko i email są wymagane."})

        try:
            klient = Klient.objects.get(imie=imie, nazwisko=nazwisko, email=email)
            data['klient'] = klient
        except Klient.DoesNotExist:
            raise serializers.ValidationError({"non_field_errors": "Klient nie istnieje."})


        if start_date < current_date:
            raise serializers.ValidationError({"start_date": "Data rozpoczęcia rezerwacji nie może być w przeszłości."})


        if end_date < current_date:
            raise serializers.ValidationError({"end_date": "Data zakończenia rezerwacji nie może być w przeszłości."})


        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"end_date": "Data zakończenia rezerwacji nie może być wcześniejsza niż data rozpoczęcia."})


        overlapping_reservations = Reservation.objects.filter(
            car=car,
            end_date__gte=start_date,
            start_date__lte=end_date
        ).exclude(id=self.instance.id if self.instance else None)

        if overlapping_reservations.exists():
            raise serializers.ValidationError({"non_field_errors": "Ten samochód jest już zarezerwowany w wybranym terminie."})

        voucher_code = data.get('voucher_code', None)
        if voucher_code:
            try:
                voucher = Voucher.objects.get(code=voucher_code)
                if not voucher.is_valid():
                    raise serializers.ValidationError({"voucher_code": "Ten voucher nie jest ważny lub wygasł."})
                data['voucher'] = voucher
            except Voucher.DoesNotExist:
                raise serializers.ValidationError({"voucher_code": "Nieprawidłowy kod vouchera."})
        else:
            data.pop('voucher_code', None)

        return data

class FleetAvailabilityCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'marka', 'model']

class FleetAvailabilitySerializer(serializers.Serializer):
    date = serializers.DateField()
    available = serializers.BooleanField()
    reserved_cars = FleetAvailabilityCarSerializer(many=True)

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ['code', 'discount_amount', 'expiration_date', 'is_percentage']