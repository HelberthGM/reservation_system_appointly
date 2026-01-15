# Reservation System API

Backend API para gestionar reservas con validación de disponibilidad
y automatización de notificaciones mediante n8n.

## Features
- Crear, listar y cancelar reservas
- Prevención de dobles reservas
- Integración con n8n para notificaciones
- API REST lista para front o automatizaciones

## Tech Stack
- Python
- Django + Django REST Framework
- n8n (webhooks y automatización)

## API Endpoints
POST   /api/reservations/
GET    /api/reservations/
DELETE /api/reservations/{id}/

## Example Payload
```json
{
  "client_name": "Juan Pérez",
  "client_email": "juan@email.com",
  "date": "2026-02-10",
  "time": "15:00"
}
```
## Why this matters

This project demonstrates real-world backend practices:
business rules, automation, and clean API design.