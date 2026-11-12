# 🐾 PetCare — Sistema de Gestión Clínica Veterinaria

**Evaluación Parcial N°3 — Desarrollo Backend (INACAP)**  
* **Docente:** Marcelo Alvarado Aravena  
* **Estudiante:** José L. Fica  
* **Ponderación:** 30% de la nota final

---

## 📋 Descripción del Proyecto
**PetCare** es una plataforma Fullstack diseñada para digitalizar la operación de una clínica veterinaria. Resuelve problemas críticos como el solapamiento de citas, la pérdida de fichas clínicas en papel y la falta de seguimiento en vacunación, integrando un panel administrativo completo con un portal público para clientes.

---

## 🚀 Stack Tecnológico

| Capa | Tecnología |
| :--- | :--- |
| **Backend** | Django 5 + Django REST Framework |
| **Base de Datos** | PostgreSQL 16 |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla + Fetch API) + Bootstrap 5.3 |
| **Servidor de Aplicación** | Gunicorn |
| **Servidor Web / Proxy** | Nginx |
| **Infraestructura** | AWS EC2 (Ubuntu Server 22.04) |
| **Arquitectura** | Monolito con API REST integrada |

---

## ☁️ Despliegue en AWS EC2 (Aplicación en Vivo)

* **Portal de Clientes (Público):** [http://34.199.34.121/portal/](http://34.199.34.121/portal/)
* **Acceso Personal (Staff):** [http://34.199.34.121/](http://34.199.34.121/)
* **Panel de Administración:** [http://34.199.34.121/admin/](http://34.199.34.121/admin/)
* **Arquitectura en EC2:** Nginx (puerto 80) -> Gunicorn (socket unix) -> Django -> PostgreSQL (localhost).
* **Archivos estáticos:** Servidos por Nginx desde `/home/ubuntu/petcare-eva3/staticfiles/`.

---

## ⚙️ Funcionalidades Clave

1. **Portal de Clientes (API REST):** Interfaz pública donde los clientes pueden auto-registrarse, registrar su mascota y agendar horas sin necesidad de iniciar sesión.
2. **Gestión de Entidades:** CRUD completo de Tutores, Mascotas, Profesionales y Disponibilidades.
3. **Agendamiento Inteligente:** Creación de citas con validación estricta de disponibilidad horaria y anti-solapamiento.
4. **Ficha Clínica Digital:** Registro de diagnósticos, tratamientos, recetas y exámenes asociados a una cita.
5. **Recordatorios Automáticos:** Generación automática de un control periódico (180 días) al guardar una ficha clínica (vía `signals.py`).
6. **Seguridad Basada en Roles:** Gestión de permisos diferenciados (Admin, Veterinario, Recepcionista) en backend y frontend.
7. **Django Admin Personalizado:** Panel administrativo con filtros, búsquedas avanzadas, inlines y diseño adaptado a la marca.

---

## 🛡️ Reglas de Negocio Implementadas
El sistema cuenta con validaciones robustas a nivel de modelo (ORM):
* **Anti-solapamiento:** Un profesional no puede tener dos citas que se crucen en el tiempo.
* **Disponibilidad:** La cita debe caer dentro de un bloque horario configurado para el profesional.
* **Fecha:** No se permiten agendar citas en el pasado.

---

## 👥 Roles y Usuarios Demo

El sistema define 3 roles con permisos diferenciados. Todos usan la contraseña: `petcare2024`

| Usuario | Rol | Acceso |
| :--- | :--- | :--- |
| `admin_petcare` | **Administrador** | Todos los modelos. Acceso total al `/admin/`. |
| `vet_petcare` | **Veterinario** | Mascotas, Citas, Fichas Clínicas y Recordatorios. |
| `recepcion_petcare` | **Recepcionista** | Tutores, Mascotas y Citas (sin acceso a fichas clínicas). |

### 🔒 Seguridad de Sesiones
Para proteger la confidencialidad de las fichas clínicas, el sistema cuenta con un tiempo de expiración de sesión por inactividad. 
*   **Expiración:** 60 minutos.
*   **Implementación:** Configurado en `settings.py` (`SESSION_COOKIE_AGE` y `SESSION_SAVE_EVERY_REQUEST`).

---

## 🛠️ Ejecución Local (Windows)

Sigue estos pasos para correr el proyecto en tu entorno local:

### 1. Clonar el repositorio
```powershell
git clone https://github.com/joselfica/petcare-eva3.git
cd petcare-eva3