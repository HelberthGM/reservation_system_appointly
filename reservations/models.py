from django.db import models

class Reservation(models.Model):

    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Sin confirmar'),
        (STATUS_CONFIRMED, 'Confirmado'),
        (STATUS_CANCELLED, 'Cancelado'),
    ]

    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.date} {self.time} ({self.get_status_display()})"
