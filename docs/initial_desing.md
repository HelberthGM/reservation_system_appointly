# Diseño inicial

## Casos de uso del sistema de reservas (MVP)

1. Crear una reserva

* Un cliente envía nombre, email, fecha y hora de reserva
* El sistema valida:
  - El formato del email
  - La fecha y hora están en el futuro
  - No hay reservas existentes en el mismo horario
* Si está libre → guarda la reserva con estado "confirmado"
* Si no → rechaza con mensaje claro

2. Ver reservas

* El negocio consulta las reservas de una fecha o todas
* El sistema devuelve la lista ordenada por fecha y hora
* Opcional: Filtrar por estado (confirmado/cancelado)

3. Cancelar una reserva

* El negocio elimina una reserva existente
* El sistema actualiza el estado a "cancelado"
* El sistema libera el horario para nuevas reservas

## Modelos de datos
### Reservation

- id_reserva
- name
- email
- date
- time
- status (por confirmar/confirmado/cancelado)