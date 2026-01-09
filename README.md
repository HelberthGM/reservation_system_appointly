# Sistema de Reservas Simple (Backend + Automatización)

## 📌 Descripción

Sistema de reservas sencillo y robusto para **servicios pequeños** (clases, consultorios, entrenadores, salas de reunión) que permite **crear, validar y cancelar reservas**, evitando conflictos de horario y enviando **notificaciones automáticas**.

El enfoque es **API-first** con automatización: el backend gestiona la lógica crítica y n8n se encarga de confirmaciones y flujos externos.

---

## 🎯 Problema que resuelve

Muchos negocios gestionan reservas manualmente (WhatsApp, Excel, Google Calendar), lo que genera:

* Doble reserva del mismo horario
* Errores humanos
* Falta de confirmaciones automáticas

Este sistema elimina esos problemas con reglas claras y automatización.

---

## ✅ Qué hace

* Crear reservas vía API
* Evitar doble reserva en el mismo horario
* Listar reservas por fecha
* Cancelar reservas
* Enviar confirmaciones y notificaciones automáticas (vía n8n)

## ❌ Qué NO hace (por diseño)

* No gestiona pagos
* No incluye autenticación avanzada
* No maneja múltiples sedes

> Estas decisiones mantienen el sistema **simple, mantenible y fácil de adaptar**.

---

## 🧱 Arquitectura

```
Cliente (Formulario / Postman / n8n)
        ↓
Backend API (FastAPI)
        ↓
Base de datos (SQLite / PostgreSQL)
        ↓
n8n (emails, recordatorios, automatización)
```

---

## 🔌 Endpoints principales

### Crear reserva

```http
POST /reservations
```

**Body (JSON):**

```json
{
  "name": "Juan Pérez",
  "email": "juan@email.com",
  "date": "2026-01-15",
  "time": "10:00"
}
```

### Listar reservas por fecha

```http
GET /reservations?date=2026-01-15
```

### Cancelar reserva

```http
DELETE /reservations/{id}
```

---

## 🧠 Reglas de negocio

* No se permiten dos reservas en la misma fecha y hora
* Todos los campos son validados antes de guardar
* El sistema responde rápido y procesa notificaciones en segundo plano

---

## 🤖 Automatización con n8n

* Recepción de reservas vía Webhook
* Envío de confirmación automática
* Manejo de errores sin romper el flujo
* Posibilidad de añadir recordatorios o integraciones (Google Sheets, email, WhatsApp)

---

## 🧪 Pruebas

* Probado usando Postman y Swagger UI
* Flujo probado con datos incompletos y campos extra
* Manejo de errores controlado

---

## 🚀 Casos de uso

* Clases particulares
* Entrenadores personales
* Consultorios pequeños
* Reservas internas de salas

---

## 💼 Enfoque profesional

Este proyecto está pensado como **base vendible**, fácilmente adaptable a distintos negocios y escalable con:

* PostgreSQL
* Docker
* Autenticación
* Frontend dedicado

---

## 📈 Estado del proyecto

✔ MVP funcional
✔ Backend estable
✔ Automatización integrada

---

## 📬 Contacto

Proyecto desarrollado como base para soluciones freelance de automatización y backend.

---

> "Simple por fuera, sólido por dentro."
