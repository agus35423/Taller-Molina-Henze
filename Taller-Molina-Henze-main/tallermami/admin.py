from django.contrib import admin, messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone

from .models import (
    Trabajo,
    Trabajador,
    Cliente,
    Turno,
    Presupuesto,
    RepuestoPresupuestado,
    RepuestoUtilizado,
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
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm(
            "tallermami.delete_turno"
        )
# ==========================================================
# REPUESTOS DEL PRESUPUESTO
# ==========================================================

class RepuestoPresupuestadoInline(admin.TabularInline):
    model = RepuestoPresupuestado
    extra = 1


class RepuestoUtilizadoInline(admin.TabularInline):
    model = RepuestoUtilizado
    extra = 1


# ==========================================================
# PRESUPUESTOS
# ==========================================================

@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "turno",
        "estado",
        "mano_obra_estimada",
        "mostrar_total_estimado",
        "mostrar_total_final",
        "final_enviado",
    )

    list_filter = ("estado", "final_enviado")
    search_fields = ("turno__patente", "turno__vehiculo")
    readonly_fields = (
        "token",
        "fecha_envio",
        "fecha_respuesta",
        "fecha_finalizacion",
    )

    fields = (
        "turno",
        "estado",
        "mano_obra_estimada",
        "observaciones",
        "token",
        "fecha_envio",
        "fecha_respuesta",
        "mano_obra_final",
        "detalle_final",
        "fecha_finalizacion",
        "final_enviado",
    )

    inlines = [
        RepuestoPresupuestadoInline,
        RepuestoUtilizadoInline,
    ]

    actions = [
        "enviar_presupuesto",
        "enviar_detalle_final",
    ]

    @admin.display(description="Total estimado")
    def mostrar_total_estimado(self, obj):
        return f"${obj.total_estimado():,.2f}"

    @admin.display(description="Total final")
    def mostrar_total_final(self, obj):
        return f"${obj.total_final():,.2f}"

    
    @admin.action(description="Enviar presupuesto al cliente")
    def enviar_presupuesto(self, request, queryset):
        for presupuesto in queryset.select_related(
            "turno", "turno__usuario"
        ):
            turno = presupuesto.turno
            email = ""

            # Buscar primero el correo del usuario asociado al turno
            if turno.usuario and turno.usuario.email:
                email = turno.usuario.email.strip()

            # Si no hay correo en User, buscar una coincidencia
            # exacta de nombre y apellido en Cliente.
            if not email and turno.usuario:
                nombre = turno.usuario.first_name.strip()
                apellido = turno.usuario.last_name.strip()

                if nombre and apellido:
                    clientes = Cliente.objects.filter(
                        nombre__iexact=nombre,
                        apellido__iexact=apellido,
                    ).exclude(email="")

                    if clientes.count() == 1:
                        email = clientes.first().email.strip()

            if not email:
                self.message_user(
                    request,
                    f"El turno #{turno.id} no tiene un correo "
                    "identificable. Revisá el email del usuario "
                    "asociado al turno.",
                    level=messages.ERROR,
                )
                continue

            if presupuesto.estado != "pendiente":
                self.message_user(
                    request,
                    f"El presupuesto del turno #{turno.id} "
                    "ya fue respondido.",
                    level=messages.WARNING,
                )
                continue

            aceptar = request.build_absolute_uri(
                reverse(
                    "responder_presupuesto",
                    args=[presupuesto.token, "aceptar"],
                )
            )
            rechazar = request.build_absolute_uri(
                reverse(
                    "responder_presupuesto",
                    args=[presupuesto.token, "rechazar"],
                )
            )

            lineas = [
                f"- {item.nombre}: {item.cantidad} x "
                f"${item.precio_unitario:.2f} = "
                f"${item.subtotal():.2f}"
                for item in presupuesto.repuestos_estimados.all()
            ]

            detalle_repuestos = (
                "\n".join(lineas)
                if lineas else "No se cargaron repuestos."
            )

            mensaje = (
                f"Hola:\n\n"
                f"Presupuesto para el vehículo {turno.vehiculo} "
                f"(patente {turno.patente}).\n\n"
                f"Repuestos:\n{detalle_repuestos}\n\n"
                f"Mano de obra: ${presupuesto.mano_obra_estimada:.2f}\n"
                f"TOTAL ESTIMADO: ${presupuesto.total_estimado():.2f}\n\n"
                f"Observaciones: "
                f"{presupuesto.observaciones or 'Sin observaciones'}\n\n"
                "Para aceptar el presupuesto, ingresá aquí:\n"
                f"{aceptar}\n\n"
                "Para rechazarlo, ingresá aquí:\n"
                f"{rechazar}\n\n"
                "La reparación no se autorizará hasta que confirmes "
                "tu decisión.\n\n"
                "Taller Molina Henze"
            )

            try:
                send_mail(
                    subject="Presupuesto de reparación - Taller Molina Henze",
                    message=mensaje,
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False,
                )

                presupuesto.fecha_envio = timezone.now()
                presupuesto.save(update_fields=["fecha_envio"])

                turno.estado = "presupuesto_pendiente"
                turno.save(update_fields=["estado"])

                self.message_user(
                    request,
                    f"Se envió el presupuesto del turno #{turno.id}.",
                    level=messages.SUCCESS,
                )
            except Exception as error:
                self.message_user(
                    request,
                    f"No se pudo enviar el presupuesto del turno "
                    f"#{turno.id}: {error}",
                    level=messages.ERROR,
                )

    @admin.action(description="Enviar detalle de reparación finalizada")
    def enviar_detalle_final(self, request, queryset):
        for presupuesto in queryset.select_related(
            "turno", "turno__usuario"
        ):
            turno = presupuesto.turno
            email = ""

            if turno.usuario and turno.usuario.email:
                email = turno.usuario.email.strip()

            if not email and turno.usuario:
                nombre = turno.usuario.first_name.strip()
                apellido = turno.usuario.last_name.strip()

                if nombre and apellido:
                    clientes = Cliente.objects.filter(
                        nombre__iexact=nombre,
                        apellido__iexact=apellido,
                    ).exclude(email="")

                    if clientes.count() == 1:
                        email = clientes.first().email.strip()

            if presupuesto.estado != "aceptado":
                self.message_user(
                    request,
                    f"El turno #{turno.id} no tiene un presupuesto aceptado.",
                    level=messages.ERROR,
                )
                continue

            if not email:
                self.message_user(
                    request,
                    f"No se encontró un correo identificable para "
                    f"el turno #{turno.id}.",
                    level=messages.ERROR,
                )
                continue

            if presupuesto.final_enviado:
                self.message_user(
                    request,
                    f"El detalle final del turno #{turno.id} ya fue enviado.",
                    level=messages.WARNING,
                )
                continue

            lineas = [
                f"- {item.nombre}: {item.cantidad} x "
                f"${item.precio_unitario:.2f} = "
                f"${item.subtotal():.2f}"
                for item in presupuesto.repuestos_utilizados.all()
            ]

            detalle_repuestos = (
                "\n".join(lineas)
                if lineas
                else "No se registraron repuestos utilizados."
            )

            mensaje = (
                "Hola:\n\n"
                f"Finalizamos la reparación de tu vehículo "
                f"{turno.vehiculo}, patente {turno.patente}.\n\n"
                f"Repuestos utilizados:\n{detalle_repuestos}\n\n"
                f"Mano de obra final: ${presupuesto.mano_obra_final:.2f}\n"
                f"TOTAL FINAL: ${presupuesto.total_final():.2f}\n\n"
                f"Detalle del trabajo: "
                f"{presupuesto.detalle_final or 'Sin detalles adicionales'}\n\n"
                "Gracias por confiar en Taller Molina Henze."
            )

            try:
                send_mail(
                    subject="Reparación finalizada - Taller Molina Henze",
                    message=mensaje,
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False,
                )

                presupuesto.final_enviado = True
                presupuesto.fecha_finalizacion = timezone.now()
                presupuesto.save(
                    update_fields=[
                        "final_enviado",
                        "fecha_finalizacion",
                    ]
                )

                turno.estado = "finalizado"
                turno.porcentaje_reparacion = 100
                turno.save(
                    update_fields=[
                        "estado",
                        "porcentaje_reparacion",
                    ]
                )

                self.message_user(
                    request,
                    f"Se envió el detalle final del turno #{turno.id}.",
                    level=messages.SUCCESS,
                )
            except Exception as error:
                self.message_user(
                    request,
                    f"No se pudo enviar el detalle del turno "
                    f"#{turno.id}: {error}",
                    level=messages.ERROR,
                )
