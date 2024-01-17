from datetime import timedelta

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from .models import Car
from .serializers import CarSerializer
class ListCarView(generics.ListCreateAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        queryset = Car.objects.filter(dostepny=True)

        marka = self.request.query_params.get('marka', None)
        if marka:
            queryset = queryset.filter(marka__icontains=marka)

        model = self.request.query_params.get('model', None)
        if model:
            queryset = queryset.filter(model__icontains=model)

        rok_produkcji = self.request.query_params.get('rok_produkcji', None)
        if rok_produkcji:
            queryset = queryset.filter(rok_produkcji=rok_produkcji)

        return queryset

class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.filter(dostepny=True)
    serializer_class = CarSerializer
    permission_classes = [IsAdminUser]