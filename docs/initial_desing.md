# Diseño inicial 

## Casos de uso del sistema de reservas (MVP)

1. Crear una reserva

* Un cliente envía nombre, email, fecha y hora de reserva
* El sistema valida disponibilidad
* Si está libre → guarda la reserva
* Si no → rechaza con mensaje claro

2. Ver reservas 

* El negocio consulta las reservas de una fecha o todas
* El sistema devuelve la lista ordenada

3. Cancelar una reserva
* El negocio elimina una reserva existente
* El sistema libera el horario

## Modelos de datos
### Reservation

- id_reserva
- name
- email
- date
- time