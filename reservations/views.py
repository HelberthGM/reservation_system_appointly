from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
import requests


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all().order_by('date', 'time')
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        reservation = serializer.save()
        
        # token para email
        signer = TimestampSigner()
        signed_id = signer.sign(str(reservation.id))

        BASE_URL = settings.FRONTEND_URL
        confirm_url = f"{BASE_URL}/api/reservations/confirm/?token={signed_id}"
        cancel_url = f"{BASE_URL}/api/reservations/cancel/?token={signed_id}"

        try:
            requests.post(
                "http://localhost:5678/webhook-test/reservation_created",
                json={
                    "client_name": reservation.client_name,
                    "client_email": reservation.client_email,
                    "date": str(reservation.date),
                    "time": str(reservation.time),
                    "confirm_url": confirm_url,
                    "cancel_url": cancel_url,
                },
                timeout=3
            )
        except requests.exceptions.RequestException:
            # la reserva NO falla si n8n está caído
            pass



class ReservationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    #permission_classes = [permissions.IsAdminUser]

class ReservationConfirmView(APIView):
    def get(self, request, signed_id):
        signer = TimestampSigner()

        try:
            reservation_id = signer.unsign(
                signed_id,
                max_age=60 * 60 * 24  # 24 horas
            )
        except SignatureExpired:
            return Response(
                {"error": "El enlace expiró"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except BadSignature:
            return Response(
                {"error": "Enlace inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "signed_id": signed_id,
            "message": "Haga click para confirmar reserva..."
        })
    
    def post(self, request):
        signed_id = request.data.get("signed_id")
        signer = TimestampSigner()
        try:
            reservation_id = signer.unsign(
                signed_id,
                max_age=60 * 60 * 24
            )
        except SignatureExpired:
            return Response(
                {"error": "El enlace expiró"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except BadSignature:
            return Response(
                {"error": "Enlace inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        reservation = get_object_or_404(Reservation, id=reservation_id)
        if reservation.status == "confirmed":
            return Response(
                {"message": "La reserva ya estaba confirmada"}
            )
        
        if reservation.status == "cancelled":
            return Response(
                {"error": "No se puede confirmar una reserva cancelada"},
                status=status.HTTP_400_BAD_REQUEST
            )
        reservation.status = "confirmed"
        reservation.save()
        return Response({"message": "Reserva confirmada exitosamente."})

class ReservationCancelView(APIView):
    def get(self, request, signed_id):
        signer = TimestampSigner()

        try:
            reservation_id = signer.unsign(
                signed_id,
                max_age=60 * 60 * 24  # 24 horas
            )
        except SignatureExpired:
            return Response(
                {"error": "El enlace expiró"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except BadSignature:
            return Response(
                {"error": "Enlace inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "signed_id": signed_id,
            "message": "haga click para cancelar reserva..."
        })

    def post(self, request, signed_id):
        signer = TimestampSigner()

        try:
            reservation_id = signer.unsign(
                signed_id,
                max_age=60 * 60 * 24  # 24 horas
            )
        except SignatureExpired:
            return Response(
                {"error": "El enlace expiró"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except BadSignature:
            return Response(
                {"error": "Enlace inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation = get_object_or_404(Reservation, id=reservation_id)

        if reservation.status == "cancelled":
            return Response(
                {"message": "La reserva ya está cancelada"}
            )

        reservation.status = "cancelled"
        reservation.save()

        return Response({
            "signed_id": signed_id,
            "message": "La reserva ha sido cancelada exitosamente."
        })
