from rest_framework import serializers
from datetime import date
from .models import Klient

class KlientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klient
        fields = '__all__'

    def validate_data_urodzenia(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("Klient musi być pełnoletni (18 lat lub więcej).")
        return value

    def validate_email(self, value):
        if Klient.objects.filter(email=value).exists():
            raise serializers.ValidationError("Klient z tym adresem email już istnieje.")
        return value

class KlientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klient
        fields = ['imie', 'nazwisko', 'prawo_jazdy_numer', 'data_urodzenia', 'numer_telefonu', 'email']

    def validate_data_urodzenia(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("Klient musi być pełnoletni (18 lat lub więcej).")
        return value

    def validate_email(self, value):
        if Klient.objects.filter(email=value).exists():
            raise serializers.ValidationError("Klient z tym adresem email już istnieje.")
        return value
