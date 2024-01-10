from rest_framework import serializers
from .models import Samochod, Rezerwacja

class SamochodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Samochod
        fields = '__all__'

class RezerwacjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rezerwacja
        fields = '__all__'

class FleetAvailabilityCarSerializer(serializers.ModelSerializer):
    marka = serializers.CharField(source='samochod__marka', default='')
    model = serializers.CharField(source='samochod__model', default='')

    class Meta:
        model = Samochod
        fields = ['id', 'marka', 'model']

class FleetAvailabilitySerializer(serializers.Serializer):
    date = serializers.DateField()
    available = serializers.BooleanField()
    reserved_cars = FleetAvailabilityCarSerializer(many=True)