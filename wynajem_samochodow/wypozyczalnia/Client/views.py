from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Klient
from .serializers import KlientSerializer, KlientCreateSerializer


class KlientListView(generics.ListAPIView):
    queryset = Klient.objects.all()
    serializer_class = KlientSerializer

class KlientCreateView(generics.CreateAPIView):
    queryset = Klient.objects.all()
    serializer_class = KlientCreateSerializer

class KlientRetrieveView(generics.RetrieveAPIView):
    queryset = Klient.objects.all()
    serializer_class = KlientSerializer

class KlientUpdateView(generics.UpdateAPIView):
    queryset = Klient.objects.all()
    serializer_class = KlientSerializer

class KlientDeleteView(generics.DestroyAPIView):
    queryset = Klient.objects.all()
    serializer_class = KlientSerializer
    permission_classes = [IsAdminUser]
