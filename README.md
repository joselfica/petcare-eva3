# PetCare — Sistema de Gestión Veterinaria

Proyecto de Evaluación Parcial N°3 — Desarrollo Backend (INACAP).

Sistema de gestión de citas y fichas médicas para la clínica veterinaria
**PetCare**. Resuelve el solapamiento de citas, la pérdida de fichas
clínicas en papel y la falta de seguimiento en vacunación.

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Django 5 + Django REST Framework |
| Base de Datos | PostgreSQL 16 |
| Frontend | Templates Django + Bootstrap 5 |
| Servidor de aplicación | Gunicorn |
| Reverse proxy | Nginx |
| Despliegue | AWS EC2 (Ubuntu 22.04) |

## Funcionalidades

1. CRUD y administración de Tutores y Mascotas.
2. Agendamiento de citas con disponibilidad por profesional.
3. Ficha clínica digital (diagnósticos, tratamientos, recetas, exámenes).
4. Recordatorios de vacunación y controles periódicos.

## Roles y usuarios demo

El sistema define 3 roles con permisos diferenciados:

| Rol | Acceso |
|---|---|
| **Administrador** | Todos los modelos del sistema |
| **Veterinario** | Mascotas, Citas, Fichas Clínicas y Recordatorios |
| **Recepcionista** | Tutores, Mascotas y Citas (sin fichas clínicas) |

Crear los grupos y usuarios demo:

```powershell
python manage.py crear_usuarios_demo

## Ejecución local (Windows)

```powershell
# 1. Clonar repo
git clone https://github.com/joselfica/petcare-eva3.git
cd petcare-eva3

# 2. Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
Copy-Item .env.example .env
# editar .env con credenciales reales

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Ejecutar servidor
python manage.py runserver
