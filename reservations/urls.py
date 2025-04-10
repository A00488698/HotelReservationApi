from django.urls import path
from .views import HotelListAPI, CreateReservationAPI,ReservationListAPI

urlpatterns = [
    path('hotels/', HotelListAPI.as_view()),
    path('reservations/', CreateReservationAPI.as_view()),
    path('reservations/list/', ReservationListAPI.as_view()),  # 新的 GET 端点
]
