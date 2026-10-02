from django.contrib import admin
from django.http import HttpResponse

from .models import (
    Trabajo,
    Trabajador,
    Cliente,
    Turno
)


# ==========================================================
# FUNCIÓN PARA EXPORTAR TURNOS A EXCEL
# ==========================================================

@admin.action(description="Exportar turnos seleccionados a Excel")
def exportar_turnos_excel(modeladmin, request, queryset):

    from openpyxl import Workbook

    libro = Workbook()
    hoja = libro.active
    hoja.title = "Turnos"

    encabezados = [
        "ID",
        "Cliente",
        "Email",
        "Vehículo",
        "Patente",
        "Servicio",
        "Trabajador",
        "Fecha",
        "Hora",
        "Estado",
        "Avance",
        "Observaciones",
    ]

    hoja.append(encabezados)

    for turno in queryset:

        if turno.usuario:
            nombre_cliente = (
                turno.usuario.get_full_name()
                or turno.usuario.username
            )

            email = turno.usuario.email

        else:
            nombre_cliente = "Sin usuario"
            email = ""

        hoja.append([
            turno.id,
            nombre_cliente,
            email,
            turno.vehiculo,
            turno.patente,
            str(turno.servicio),

            # TRABAJADOR ASIGNADO
            str(turno.trabajador)
            if turno.trabajador
            else "Sin asignar",

            turno.fecha_turno.strftime("%d/%m/%Y"),
            turno.fecha_turno.strftime("%H:%M"),
            turno.get_estado_display(),
            f"{turno.porcentaje_reparacion}%",
            turno.observaciones,
        ])

    # Ajustar ancho de columnas
    for columna in hoja.columns:

        maximo = 0
        letra = columna[0].column_letter

        for celda in columna:

            if celda.value:
                maximo = max(
                    maximo,
                    len(str(celda.value))
                )

        hoja.column_dimensions[letra].width = min(
            maximo + 2,
            40
        )

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="turnos_seleccionados.xlsx"'
    )

    libro.save(response)

    return response

    # ======================================================
    # AJUSTAR ANCHO DE LAS COLUMNAS
    # ======================================================

    for columna in hoja.columns:

        maximo = 0
        letra = columna[0].column_letter

        for celda in columna:

            if celda.value:
                maximo = max(
                    maximo,
                    len(str(celda.value))
                )

        hoja.column_dimensions[letra].width = min(
            maximo + 2,
            40
        )

    # ======================================================
    # CREAR ARCHIVO EXCEL
    # ======================================================

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="turnos_seleccionados.xlsx"'
    )

    libro.save(response)

    return response


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
        "trabajador",
        "fecha_turno",
        "estado",
        "porcentaje_reparacion",
    )

    list_filter = (
        "estado",
        "fecha_turno",
        "servicio",
        "trabajador",
    )

    search_fields = (
        "usuario__username",
        "usuario__email",
        "vehiculo",
        "patente",
        "servicio__nombre",
        "trabajador__nombre",
        "trabajador__apellido",
    )

    # Permite cambiar estos datos directamente desde la lista
    list_editable = (
        "trabajador",
        "estado",
        "porcentaje_reparacion",
    )

    ordering = (
        "-fecha_turno",
    )

    fields = (
        "usuario",
        "vehiculo",
        "patente",
        "servicio",
        "trabajador",
        "fecha_turno",
        "estado",
        "porcentaje_reparacion",
        "observaciones",
    )

    actions = [
        exportar_turnos_excel,
    ]