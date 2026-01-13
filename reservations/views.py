from rest_framework import generics, permissions
from .models import Reservation
from .serializers import ReservationSerializer

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all().order_by('date', 'time')
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]


class ReservationDeleteView(generics.DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    #permission_classes = [permissions.IsAuthenticated]
