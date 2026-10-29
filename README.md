# 🐾 PetCare — Sistema de Gestión Clínica Veterinaria

**Evaluación Parcial N°3 — Desarrollo Backend (INACAP)**
* **Docente:** Marcelo Alvarado Aravena
* **Estudiante:** José L. Fica *(ajusta tu nombre si es necesario)*
* **Ponderación:** 30% de la nota final

---

## 📋 Descripción del Proyecto
PetCare es una aplicación web Fullstack desarrollada para resolver los problemas operativos de una clínica veterinaria (solapamiento de citas, pérdida de fichas clínicas en papel y falta de seguimiento de vacunas). 

El sistema centraliza la operación clínica permitiendo la administración de tutores, mascotas, agenda médica, fichas clínicas digitales y recordatorios automáticos.

---

## 🚀 Stack Tecnológico

| Capa | Tecnología |
| :--- | :--- |
| **Backend** | Django 5 + Django REST Framework |
| **Base de Datos** | PostgreSQL 16 |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) + Bootstrap 5.3 |
| **Servidor de Aplicación** | Gunicorn |
| **Servidor Web / Proxy** | Nginx |
| **Infraestructura** | AWS EC2 (Ubuntu Server 22.04) |

---

## ⚙️ Funcionalidades Clave

1. **Gestión de Entidades:** CRUD completo de Tutores, Mascotas, Profesionales y Disponibilidades.
2. **Agendamiento Inteligente:** Creación de citas con validación estricta de disponibilidad horaria por profesional.
3. **Ficha Clínica Digital:** Registro de diagnósticos, tratamientos, recetas y exámenes asociados a una cita.
4. **Recordatorios Automáticos:** Generación automática de un control periódico (180 días) al guardar una ficha clínica.
5. **Seguridad Basada en Roles:** Gestión de permisos diferenciados para Administradores, Veterinarios y Recepcionistas.
6. **Django Admin Personalizado:** Panel administrativo con filtros, búsquedas avanzadas, inlines y diseño adaptado a la marca PetCare.

---

## 🛡️ Reglas de Negocio Implementadas
El sistema cuenta con validaciones robustas en el modelo `Cita`:
* **Anti-solapamiento:** Un profesional no puede tener dos citas que se crucen en el tiempo.
* **Disponibilidad:** La cita debe caer dentro de un bloque horario configurado para el profesional (ej. Lunes a Viernes de 09:00 a 18:00).
* **Fecha:** No se permiten agendar citas en el pasado.

---

## 👥 Roles y usuarios demo

El sistema define 3 roles con permisos diferenciados:

| Rol | Acceso |
| :--- | :--- |
| **Administrador** | Todos los modelos del sistema |
| **Veterinario** | Mascotas, Citas, Fichas Clínicas y Recordatorios |
| **Recepcionista** | Tutores, Mascotas y Citas (sin fichas clínicas) |

Comando para crear los grupos y usuarios demo:
```powershell
python manage.py crear_usuarios_demo