from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status

from .models import Samochod, Rezerwacja
from .serializers import SamochodSerializer, RezerwacjaSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lista_samochodow(request):
    if request.method == 'GET':
        samochody = Samochod.objects.filter(dostepny=True)
        serializer = SamochodSerializer(samochody, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SamochodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListaRezerwacjiView(generics.ListCreateAPIView):
    queryset = Rezerwacja.objects.all()
    serializer_class = RezerwacjaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NowaRezerwacjaView(generics.CreateAPIView):
    serializer_class = RezerwacjaSerializer
    permission_classes = [IsAuthenticated]

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
