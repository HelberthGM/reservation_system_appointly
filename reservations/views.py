from rest_framework import generics, permissions
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from django.shortcuts import get_object_or_404

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all().order_by('date', 'time')
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]

class ReservationRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    #permission_classes = [permissions.IsAdminUser]

class ReservationConfirmView(APIView):
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)

        if reservation.status == "confirmed":
            return Response(
                {"detail": "La reserva ya está confirmada."},
                status=http_status.HTTP_400_BAD_REQUEST
            )

        reservation.status = "confirmed"
        reservation.save()

        return Response(
            {"detail": "Reserva confirmada correctamente."},
            status=http_status.HTTP_200_OK
        )

class ReservationCancelView(APIView):
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)

        if reservation.status == "cancelled":
            return Response(
                {"detail": "La reserva ya está cancelada."},
                status=http_status.HTTP_400_BAD_REQUEST
            )

        reservation.status = "cancelled"
        reservation.save()

        return Response(
            {"detail": "Reserva cancelada correctamente."},
            status=http_status.HTTP_200_OK
        )
