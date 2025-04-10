from rest_framework import generics
from reservations.models import Hotel, Reservation
from reservations.serializers import HotelSerializer, ReservationSerializer

class HotelListAPI(generics.ListAPIView):
    queryset = Hotel.objects.filter(available=True)
    serializer_class = HotelSerializer

class CreateReservationAPI(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer