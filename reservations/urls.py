from django.urls import path
from .views import (
    ReservationListCreateView,
    ReservationRetrieveUpdateDestroyView,
    ReservationConfirmView,
    ReservationCancelView,
)

urlpatterns = [
    # Lista todas las reservas / Crea una nueva
    path(
        "reservations/",
        ReservationListCreateView.as_view(),
        name="reservation-list-create"
    ),

    # Obtiene / actualiza / elimina una reserva específica
    path(
        "reservations/<int:pk>/",
        ReservationRetrieveUpdateDestroyView.as_view(),
        name="reservation-detail"
    ),
    # Confirma reservacion
     path(
        "reservations/<int:pk>/confirm/",
        ReservationConfirmView.as_view(),
        name="reservation-confirm"
    ),
    # Cancela reservacion
    path(
        "reservations/<int:pk>/cancel/",
        ReservationCancelView.as_view(),
        name="reservation-cancel"
    ),
]
