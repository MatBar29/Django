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
