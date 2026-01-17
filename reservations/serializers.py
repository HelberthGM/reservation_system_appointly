from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields =['status', 'created_at', 'token_used_at']

    def validate(self, data):
        date = data['date']
        time = data['time']

        exists = Reservation.objects.filter(
            date=date,
            time=time,
            status__in=["pending", "confirmed"]
        ).exists()

        if exists:
            raise serializers.ValidationError(
                "Lo sentimos, este horario ya no está disponible. Por favor, selecciona otra hora."
            )

        return data