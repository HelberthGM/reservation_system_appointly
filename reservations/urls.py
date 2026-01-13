from django.urls import path
from .views import (
    ReservationListCreateView,
    ReservationRetrieveUpdateDestroyView,
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
]
