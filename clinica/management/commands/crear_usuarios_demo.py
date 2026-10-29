"""
============================================================================
Comando de gestión: crear_usuarios_demo
----------------------------------------------------------------------------
Archivo: clinica/management/commands/crear_usuarios_demo.py
Propósito:
    Crea los 3 grupos de seguridad del sistema PetCare y asigna permisos
    según el rol. Además, crea 3 usuarios demo (uno por rol) con contraseña
    conocida para facilitar la defensa en vivo.

Grupos y permisos:
    - Administrador: todos los permisos sobre todos los modelos.
    - Veterinario: acceso completo a Mascotas, Citas, Fichas Clínicas y
      Recordatorios; lectura de Tutores y Profesionales.
    - Recepcionista: CRUD de Tutores, Mascotas y Citas; sin acceso a
      Fichas Clínicas ni a Disponibilidades.

Uso:
    python manage.py crear_usuarios_demo

Notas:
    - El comando es idempotente: si los grupos o usuarios ya existen, los
      reutiliza y solo actualiza permisos/passwords.
    - Las contraseñas demo son conocidas y débiles a propósito; NO usar en
      producción real.
============================================================================
"""

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from clinica.models import (
    Cita,
    Disponibilidad,
    FichaClinica,
    Mascota,
    Profesional,
    Recordatorio,
    Tutor,
)


class Command(BaseCommand):
    """Crea grupos, permisos y usuarios demo del sistema PetCare."""

    help = 'Crea los grupos de seguridad y 3 usuarios demo (admin, vet, recepcion).'

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def _permisos_de(self, modelo):
        """
        Retorna todos los permisos (add, change, delete, view) de un modelo.

        Args:
            modelo: clase de modelo Django.

        Returns:
            QuerySet: permisos del modelo.
        """
        ct = ContentType.objects.get_for_model(modelo)
        return Permission.objects.filter(content_type=ct)

    def _crear_grupo(self, nombre, permisos_qs):
        """
        Crea o actualiza un grupo con los permisos indicados.

        Args:
            nombre (str): nombre del grupo.
            permisos_qs (QuerySet): permisos a asignar.

        Returns:
            Group: instancia del grupo.
        """
        grupo, _ = Group.objects.get_or_create(name=nombre)
        grupo.permissions.set(permisos_qs)
        return grupo

    def _crear_usuario(self, username, email, password, grupo):
        """
        Crea o actualiza un usuario y lo asigna a un grupo.

        Args:
            username (str): nombre de usuario.
            email (str): correo.
            password (str): contraseña demo.
            grupo (Group): grupo al que pertenece.

        Returns:
            User: instancia del usuario.
        """
        user, creado = User.objects.get_or_create(
            username=username,
            defaults={'email': email},
        )
        user.email = email
        user.set_password(password)
        user.save()
        user.groups.set([grupo])
        return user

    # ------------------------------------------------------------------
    # Handler principal
    # ------------------------------------------------------------------
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Creando grupos y permisos...'))

        # ------------------------------------------------------------------
        # Grupo Administrador: todos los permisos de la app clinica
        # ------------------------------------------------------------------
        todos = Permission.objects.filter(
            content_type__app_label='clinica'
        )
        g_admin = self._crear_grupo('Administrador', todos)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Grupo "{g_admin.name}" con {g_admin.permissions.count()} permisos'))

        # ------------------------------------------------------------------
        # Grupo Veterinario
        # ------------------------------------------------------------------
        permisos_vet = (
            self._permisos_de(Mascota) |
            self._permisos_de(Cita) |
            self._permisos_de(FichaClinica) |
            self._permisos_de(Recordatorio)
        )
        g_vet = self._crear_grupo('Veterinario', permisos_vet)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Grupo "{g_vet.name}" con {g_vet.permissions.count()} permisos'))

        # ------------------------------------------------------------------
        # Grupo Recepcionista: Tutores, Mascotas y Citas (SIN fichas clínicas)
        # ------------------------------------------------------------------
        permisos_rec = (
            self._permisos_de(Tutor) |
            self._permisos_de(Mascota) |
            self._permisos_de(Cita)
            # Nota: No se incluye FichaClinica ni Recordatorio por privacidad clínica.
        )
        g_rec = self._crear_grupo('Recepcionista', permisos_rec)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Grupo "{g_rec.name}" con {g_rec.permissions.count()} permisos'))

        # ------------------------------------------------------------------
        # Usuarios demo (password: petcare2024)
        # ------------------------------------------------------------------
        self.stdout.write(self.style.MIGRATE_HEADING('Creando usuarios demo...'))
        password = 'petcare2024'

        u_admin = self._crear_usuario('admin_petcare', 'admin@petcare.cl', password, g_admin)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Usuario "{u_admin.username}" (Administrador)'))

        u_vet = self._crear_usuario('vet_petcare', 'vet@petcare.cl', password, g_vet)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Usuario "{u_vet.username}" (Veterinario)'))

        u_rec = self._crear_usuario('recepcion_petcare', 'recepcion@petcare.cl', password, g_rec)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Usuario "{u_rec.username}" (Recepcionista)'))

        # ------------------------------------------------------------------
        # Resumen
        # ------------------------------------------------------------------
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('Resumen'))
        self.stdout.write(f'  Contraseña para los 3 usuarios demo: {password}')
        self.stdout.write(f'  admin_petcare     → Administrador')
        self.stdout.write(f'  vet_petcare       → Veterinario')
        self.stdout.write(f'  recepcion_petcare → Recepcionista')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✔ Comando ejecutado correctamente.'))