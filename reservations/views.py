from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from rest_framework import generics
from .models import Hotel, Reservation
from .serializers import HotelSerializer, ReservationSerializer
from rest_framework.views import APIView

class HotelListAPI(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class CreateReservationAPI(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()
            print("Generated confirmation_number:", reservation.confirmation_number)
            return Response({'confirmation_number': reservation.confirmation_number}, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)  # 打印详细错误信息
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationListAPI(APIView):
    def get(self, request, format=None):
        # 例如可以获取所有预订记录，或者你可以根据需求进行筛选（例如最新的几个）
        reservations = Reservation.objects.all().order_by('-id')
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
