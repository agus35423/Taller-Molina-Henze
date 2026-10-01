from django.contrib import admin

from .models import (
    Trabajo,
    Trabajador,
    Cliente,
    Turno
)


# ==========================================================
# TRABAJOS
# ==========================================================

@admin.register(Trabajo)
class TrabajoAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "precio_estimado",
    )

    search_fields = (
        "nombre",
        "descripcion",
    )


# ==========================================================
# TRABAJADORES
# ==========================================================

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "apellido",
        "especialidad",
        "telefono",
    )

    search_fields = (
        "nombre",
        "apellido",
        "especialidad",
    )


# ==========================================================
# CLIENTES
# ==========================================================

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "apellido",
        "email",
        "telefono",
    )

    search_fields = (
        "nombre",
        "apellido",
        "email",
        "telefono",
    )


# ==========================================================
# TURNOS
# ==========================================================

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "usuario",
        "vehiculo",
        "patente",
        "servicio",
        "fecha_turno",
        "estado",
        "porcentaje_reparacion",
    )

    list_filter = (
        "estado",
        "fecha_turno",
        "servicio",
    )

    search_fields = (
        "usuario__username",
        "usuario__email",
        "vehiculo",
        "patente",
        "servicio__nombre",
    )

    list_editable = (
        "estado",
        "porcentaje_reparacion",
    )

    ordering = (
        "-fecha_turno",
    )