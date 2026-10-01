from django.urls import path

from . import views


urlpatterns = [

    # ======================================================
    # INICIO
    # ======================================================

    path(
        "",
        views.inicio,
        name="inicio"
    ),


    # ======================================================
    # AUTENTICACIÓN
    # ======================================================

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "registro/",
        views.registro,
        name="registro"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    # ======================================================
    # TURNOS
    # ======================================================

    path(
        "solicitar-turno/",
        views.solicitar_turno,
        name="solicitar_turno"
    ),

    path(
        "turno-exitoso/<int:turno_id>/",
        views.turno_exitoso,
        name="turno_exitoso"
    ),

    path(
        "mis-turnos/",
        views.mis_turnos,
        name="mis_turnos"
    ),


    # ======================================================
    # ESTADO DEL VEHÍCULO
    # ======================================================

    path(
        "estado-reparacion/",
        views.estado_reparacion,
        name="estado_reparacion"
    ),


    # ======================================================
    # PDF
    # ======================================================

    path(
        "descargar-pdf/<int:turno_id>/",
        views.descargar_pdf,
        name="descargar_pdf"
    ),


    # ======================================================
    # EXCEL
    # ======================================================

    path(
        "exportar-excel/",
        views.exportar_excel,
        name="exportar_excel"
    ),

    path(
        "descargar-excel/",
        views.descargar_excel_turnos,
        name="descargar_excel_turnos"
    ),
]