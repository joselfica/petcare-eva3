# Registro de Uso de Inteligencia Artificial — PetCare EVA3

**Proyecto:** Sistema de Gestión de Citas y Fichas Médicas para Veterinaria (PetCare)
**Asignatura:** Desarrollo Backend — INACAP
**Docente:** Marcelo Alvarado Aravena
**Herramientas utilizadas:** Claude (Anthropic), ChatGPT (OpenAI), GitHub Copilot

Este documento registra las consultas realizadas a herramientas de IA
durante el desarrollo del proyecto, el resultado obtenido y los ajustes
aplicados manualmente.

---

## Fase 0 — Preparación del entorno

### Consulta 1 — Configuración de `settings.py` con PostgreSQL
- **Fecha:** _(completar)_
- **Herramienta:** Claude
- **Prompt:** "Configura un `settings.py` de Django 5 que lea credenciales de PostgreSQL desde un archivo `.env` usando python-decouple, con `ALLOWED_HOSTS` como lista y comentarios profesionales."
- **Resultado obtenido:** Bloque completo de `settings.py` con `DATABASES`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` vía `decouple`.
- **Ajustes aplicados:** Se cambió `LANGUAGE_CODE` a `es-cl` y `TIME_ZONE` a `America/Santiago`. Se agregó `REST_FRAMEWORK` con autenticación por sesión.
- **Uso en el proyecto:** `petcare/settings.py` (Fase 0, Paso 0.11).

### Consulta 2 — Resolución de error `mkdir -p` en PowerShell
- **Fecha:** _(completar)_
- **Herramienta:** Claude
- **Prompt:** "¿Por qué `mkdir -p static templates/registration templates/admin` falla en PowerShell y cómo lo reemplazo?"
- **Resultado obtenido:** Explicación del alias `-p` → `-Path` y uso de `New-Item -ItemType Directory -Force -Path`.
- **Ajustes aplicados:** Se usó `New-Item` por carpeta.
- **Uso en el proyecto:** `static/`, `templates/`, `templates/registration/`, `templates/admin/`.

---

## Fase 1 — Modelos y base de datos

### Consulta 3 — Regla de negocio anti-solapamiento en `Cita.clean()`
- **Fecha:** _(completar)_
- **Herramienta:** Claude
- **Prompt:** "Implementa en Django una validación en `Cita.clean()` que rechace solapamiento de citas del mismo profesional, considerando `duracion_min`. Debe detectar si dos intervalos [inicio, fin) se superponen."
- **Resultado obtenido:** Lógica con `timedelta`, iteración sobre citas activas y condición `inicio < otro_fin AND fin > otro_inicio`.
- **Ajustes aplicados:** Se filtró además por `estado__in=['PEND','CONF']` para ignorar canceladas. Se añadió validación de disponibilidad (regla 2) y de fecha pasada (regla 1).
- **Uso en el proyecto:** `clinica/models.py` → `Cita.clean()` (Fase 1, Paso 1.1).

### Consulta 4 — Validación de disponibilidad por profesional
- **Fecha:** _(completar)_
- **Herramienta:** Claude
- **Prompt:** "Dado un `Profesional` con bloques `Disponibilidad(dia_semana, hora_inicio, hora_fin)`, valida en `Cita.clean()` que la cita caiga dentro de algún bloque."
- **Resultado obtenido:** Filtro `disponibilidades.filter(dia_semana=..., hora_inicio__lte=hora, hora_fin__gte=hora)`.
- **Ajustes aplicados:** Se agregó un método `_dia_semana_codigo()` para mapear `datetime.weekday()` a `LUN..DOM`.
- **Uso en el proyecto:** `clinica/models.py` → `Cita.clean()` y `Cita._dia_semana_codigo()`.

### Consulta 5 — Error de indentación en consola interactiva
- **Fecha:** _(completar)_
- **Herramienta:** ChatGPT
- **Prompt:** "Al pegar un `for` con un `print` después en `python manage.py shell`, recibo `SyntaxError: invalid syntax`. ¿Por qué?"
- **Resultado obtenido:** Explicación de que en la consola todo lo que sigue a `...` es parte del bloque; se debe cerrar con Enter vacío antes de un comando nuevo.
- **Ajustes aplicados:** Se optó por crear `scripts/seed_fase1.py` y ejecutarlo con `python manage.py shell -c "exec(open(...).read())"`.
- **Uso en el proyecto:** `scripts/seed_fase1.py` (Fase 1, Paso 1.5).

---

## Fase 2 — Django Admin personalizado

### Consulta 6 — Personalización de `admin.py` con inlines y actions
- **Fecha:** _(completar)_
- **Herramienta:** Claude
- **Prompt:** "Personaliza el `admin.py` de Django para 7 modelos de una clínica veterinaria: filtros, búsquedas, inlines de Mascotas en Tutor y FichaClínica en Cita, y acciones masivas para confirmar/cancelar citas y marcar recordatorios enviados."
- **Resultado obtenido:** Estructura completa con `ModelAdmin`, `TabularInline`, `StackedInline`, `@admin.action`, `@admin.display`, `autocomplete_fields`, `date_hierarchy`.
- **Ajustes aplicados:** Se agregaron `fieldsets` para agrupar secciones. Se añadieron columnas calculadas `_edad`, `_total_mascotas`, `_tiene_ficha`, `_vencido`.
- **Uso en el proyecto:** `clinica/admin.py` (Fase 2, Paso 2.3).

### Consulta 7 — Sobreescritura del header del Admin
- **Fecha:** _(completar)_
- **Herramienta:** Claude
- **Prompt:** "¿Cómo personalizo el header del Django Admin con un logo y nombre propio, sin perder CSS ni scripts nativos?"
- **Resultado obtenido:** Extensión de `admin/base_site.html` sobrescribiendo `{% block branding %}` y `{% block title %}`, y `admin/index.html` sobrescribiendo `{% block content %}` con `{{ block.super }}`.
- **Ajustes aplicados:** Se añadieron emojis y estilos inline.
- **Uso en el proyecto:** `templates/admin/base_site.html`, `templates/admin/index.html`.

---

## Fase 3 — Seguridad, roles y permisos

### Consulta 8 — Grupos y permisos programáticos
- **Fecha:** _(completar)_
- **Herramienta:** Claude
- **Prompt:** "Crea un management command de Django idempotente que cree 3 grupos (Administrador, Veterinario, Recepcionista) con permisos diferenciados sobre 7 modelos, y 3 usuarios demo con password conocida."
- **Resultado obtenido:** Comando completo con `Group.objects.get_or_create`, `Permission.objects.filter(content_type__app_label=...)`, `User.objects.get_or_create`, `set_password`.
- **Ajustes aplicados:** Se documentó cada método con docstring y se añadieron mensajes de progreso con `self.stdout.write`.
- **Uso en el proyecto:** `clinica/management/commands/crear_usuarios_demo.py` (Fase 3, Paso 3.8).

### Consulta 9 — Login/logout con templates propios
- **Fecha:** _(completar)_
- **Herramienta:** Claude
- **Prompt:** "Configura `petcare/urls.py` para usar `LoginView` y `LogoutView` de Django con templates propios en `templates/registration/`, e incluye un formulario de login con Bootstrap."
- **Resultado obtenido:** Rutas con `auth_views.LoginView.as_view(template_name=...)` y template `login.html` con `{% csrf_token %}` y campo `next`.
- **Ajustes aplicados:** Se agregó `base.html` compartido con navbar condicional y mensajes flash.
- **Uso en el proyecto:** `petcare/urls.py`, `templates/registration/login.html`, `templates/base.html`.

---

## Reflexión final

El uso de IA se concentró en:
1. **Acelerar la configuración inicial** (settings, `.env`, estructura de carpetas).
2. **Validar reglas de negocio complejas** (solapamiento, disponibilidad).
3. **Reducir errores de sintaxis** en la consola interactiva.
4. **Generar documentación profesional** (docstrings, README, este archivo).

En todos los casos, el código generado fue **revisado, ajustado y probado** manualmente antes de integrarse al proyecto. Los ajustes propios se documentan en cada consulta.