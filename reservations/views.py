from django.conf import settings
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.views import APIView
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
        confirm_url = f"{BASE_URL}/api/reservations/confirm/?signed_id={signed_id}"
        cancel_url = f"{BASE_URL}/api/reservations/cancel/?signed_id={signed_id}"

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
    def get(self, request):
        signed_id = request.GET.get("signed_id")
        signer = TimestampSigner()

        try:
            reservation_id = signer.unsign(
                signed_id,
                max_age=60 * 60 * 24  # 24 horas
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
                    "message": "Este enlace no es valido."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return render(
            request,
            "reservations/confirm.html",
            {"signed_id": signed_id}
        )
    
    def post(self, request):
        signed_id = request.POST.get("signed_id")
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
                    "message": "Este enlace no es valido."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation = get_object_or_404(Reservation, id=reservation_id)

        if reservation.token_used_at:
            return render(
                request,
                "reservations/error.html",
                {
                    "title": "Link inválido",
                    "message": "Este enlace ya fue usado o expiró."
                },
                status=status.HTTP_410_GONE
            )

        
        if reservation.status == "confirmed":
            return render(request, "reservations/success.html", {
            "title": "Reserva ya confirmada",
            "message": "Tu reserva ha sido confirmada exitosamente."},
            status=status.HTTP_200_OK)

        
        if reservation.status == "cancelled":
            return render(
                request,
                "reservations/error.html",
                {
                    "title": "Error",
                    "message": "No se puede confirmar una reserva cancelada"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.status = "confirmed"
        reservation.save()
        reservation.mark_token_used()

        return render(request, "reservations/success.html", {
            "title": "Reserva confirmada",
            "message": "Tu reserva ha sido confirmada exitosamente."},
            status=status.HTTP_200_OK)

class ReservationCancelView(APIView):
    def get(self, request):
        signed_id = request.GET.get("signed_id")
        signer = TimestampSigner()

        try:
            reservation_id = signer.unsign(
                signed_id,
                max_age=60 * 60 * 24  # 24 horas
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
                    "message": "Este enlace no es valido."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        return render(
            request,
            "reservations/cancel.html",
            {"signed_id": signed_id}
        )

    def post(self, request):
        signed_id = request.POST.get("signed_id")

        signer = TimestampSigner()

        try:
            reservation_id = signer.unsign(
                signed_id,
                max_age=60 * 60 * 24  # 24 horas
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
                    "message": "Este enlace no es valido."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        reservation = get_object_or_404(Reservation, id=reservation_id)

        if reservation.token_used_at:
            return render(
                request,
                "reservations/error.html",
                {
                    "title": "Link inválido",
                    "message": "Este enlace ya fue usado o expiró."
                },
                status=status.HTTP_410_GONE
            )

        if reservation.status == "cancelled":
            return render(
                request,
                "reservations/error.html",
                {
                    "title": "Reserva cancelada previamente",
                    "message": "Esta reserva ya fue cancelada."
                },
                status=status.HTTP_409_CONFLICT
            )

        reservation.status = "cancelled"
        reservation.save()
        reservation.mark_token_used()

        return render(request, "reservations/success.html", {
            "title": "Reserva cancelada",
            "message": "Tu reserva ha sido cancelada exitosamente."},
            status=status.HTTP_200_OK)
