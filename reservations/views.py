from django.conf import settings
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
import requests
from drf_spectacular.utils import extend_schema

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
        confirm_url = f"{BASE_URL}/api/reservations/confirm/?signed_id={signed_id}"
        cancel_url = f"{BASE_URL}/api/reservations/cancel/?signed_id={signed_id}"

        try:
            requests.post(
                settings.N8N_WEBHOOK_URL,
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

    @extend_schema(exclude=True)
    def get(self, request):
        signed_id = request.GET.get("signed_id")
        signer = TimestampSigner()

        try:
            reservation_id = signer.unsign(
                signed_id,
                max_age=60 * 60 * 24
            )
        except SignatureExpired:
            return render(
                request,
                "reservations/error.html",
                {
                    "title": "Link inválido",
                    "message": "Este enlace ya expiró."
                },
                status=status.HTTP_410_GONE
            )
        except BadSignature:
            return render(
                request,
                "reservations/error.html",
                {
                    "title": "Link inválido",
                    "message": "Este enlace no es válido."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return render(
            request,
            "reservations/confirm.html",
            {"signed_id": signed_id}
        )

    @extend_schema(
        summary="Confirmar reserva",
        description=(
            "Confirma una reserva pendiente usando un enlace firmado. "
            "Este endpoint cambia el estado de la reserva a CONFIRMED "
            "y marca el token como usado."
        ),
        responses={
            200: {
                "type": "object",
                "example": {
                    "status": "confirmed",
                    "message": "Reserva confirmada correctamente"
                }
            },
            400: {
                "type": "object",
                "example": {
                    "error": "No se puede confirmar una reserva cancelada"
                }
            },
            410: {
                "type": "object",
                "example": {
                    "error": "El enlace ya fue usado o expiró"
                }
            }
        }
    )
    def post(self, request):
        signed_id = request.POST.get("signed_id")
        signer = TimestampSigner()

        try:
            reservation_id = signer.unsign(
                signed_id,
                max_age=60 * 60 * 24
            )
        except (SignatureExpired, BadSignature):
            return Response(
                {"error": "Enlace inválido o expirado"},
                status=status.HTTP_410_GONE
            )

        reservation = get_object_or_404(Reservation, id=reservation_id)

        if reservation.token_used_at:
            return Response(
                {"error": "Este enlace ya fue usado o expiró"},
                status=status.HTTP_410_GONE
            )

        if reservation.status == "confirmed":
            return Response(
                {
                    "status": "confirmed",
                    "message": "La reserva ya estaba confirmada"
                },
                status=status.HTTP_200_OK
            )

        if reservation.status == "cancelled":
            return Response(
                {"error": "No se puede confirmar una reserva cancelada"},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status = "confirmed"
        reservation.save()
        reservation.mark_token_used()

        return Response(
            {
                "status": "confirmed",
                "message": "Reserva confirmada correctamente"
            },
            status=status.HTTP_200_OK
        )

class ReservationCancelView(APIView):

    @extend_schema(exclude=True)
    def get(self, request):
        signed_id = request.GET.get("signed_id")
        signer = TimestampSigner()

        try:
            signer.unsign(signed_id, max_age=60 * 60 * 24)
        except (SignatureExpired, BadSignature):
            return render(
                request,
                "reservations/error.html",
                {
                    "title": "Link inválido",
                    "message": "Este enlace no es válido o expiró."
                },
                status=status.HTTP_410_GONE
            )

        return render(
            request,
            "reservations/cancel.html",
            {"signed_id": signed_id}
        )

    @extend_schema(
        summary="Cancelar reserva",
        description=(
            "Cancela una reserva pendiente usando un enlace firmado. "
            "Este endpoint cambia el estado de la reserva a CANCELLED "
            "y marca el token como usado."
        ),
        responses={
            200: {
                "type": "object",
                "example": {
                    "status": "cancelled",
                    "message": "Reserva cancelada correctamente"
                }
            },
            409: {
                "type": "object",
                "example": {
                    "error": "La reserva ya fue cancelada"
                }
            },
            410: {
                "type": "object",
                "example": {
                    "error": "El enlace ya fue usado o expiró"
                }
            }
        }
    )
    def post(self, request):
        signed_id = request.POST.get("signed_id")
        signer = TimestampSigner()

        try:
            reservation_id = signer.unsign(
                signed_id,
                max_age=60 * 60 * 24
            )
        except (SignatureExpired, BadSignature):
            return Response(
                {"error": "Enlace inválido o expirado"},
                status=status.HTTP_410_GONE
            )

        reservation = get_object_or_404(Reservation, id=reservation_id)

        if reservation.token_used_at:
            return Response(
                {"error": "Este enlace ya fue usado o expiró"},
                status=status.HTTP_410_GONE
            )

        if reservation.status == "cancelled":
            return Response(
                {"error": "La reserva ya fue cancelada"},
                status=status.HTTP_409_CONFLICT
            )

        reservation.status = "cancelled"
        reservation.save()
        reservation.mark_token_used()

        return Response(
            {
                "status": "cancelled",
                "message": "Reserva cancelada correctamente"
            },
            status=status.HTTP_200_OK
        )
