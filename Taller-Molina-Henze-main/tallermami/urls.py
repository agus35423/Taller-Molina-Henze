from django.urls import path
from django.contrib.auth import views as auth_views

from .views import vista_jefe_taller, vista_secretario

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
    
    path("jefe-taller/trabajos/", views.jefe_trabajos, name="jefe_trabajos"),
    path("jefe-taller/trabajadores/", views.jefe_trabajadores, name="jefe_trabajadores"),
    path("jefe-taller/clientes/", views.jefe_clientes, name="jefe_clientes"),
    path("jefe-taller/turnos/", views.jefe_turnos, name="jefe_turnos"),

    path("secretario/clientes/", views.secretario_clientes, name="secretario_clientes"),
    path("secretario/turnos/", views.secretario_turnos, name="secretario_turnos"),


    # ======================================================
    # AUTENTICACIÓN
    # ======================================================
    
    path(
    "jefe-taller/",
    vista_jefe_taller,
    name="vista_jefe_taller"
    ),

    path(
    "secretario/",
    vista_secretario,
    name="vista_secretario"
    ),


    path(
        "login/",
        views.login_view,
        name="login"
    ),
    # ======================================================
# RECUPERACIÓN DE CONTRASEÑA
# ======================================================

path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="tallermami/password_reset.html",
        email_template_name="tallermami/password_reset_email.txt",
        subject_template_name="tallermami/password_reset_subject.txt",
    ),
    name="password_reset"
),

path(
    "password-reset/enviado/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="tallermami/password_reset_done.html"
    ),
    name="password_reset_done"
),

path(
    "password-reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="tallermami/password_reset_confirm.html"
    ),
    name="password_reset_confirm"
),

path(
    "password-reset/completo/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="tallermami/password_reset_complete.html"
    ),
    name="password_reset_complete"
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
    path(
    "turnos/cancelar/<int:turno_id>/",
    views.cancelar_turno,
    name="cancelar_turno"
    ),

    path(
    "oferta-turno/<uuid:token>/",
    views.aceptar_oferta_turno,
    name="aceptar_oferta_turno"
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

    path(
    "presupuesto/<uuid:token>/<str:decision>/",
    views.responder_presupuesto,
    name="responder_presupuesto",
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
    "descargar-excel-turnos/",
    views.descargar_excel_turnos,
    name="descargar_excel_turnos",
    ),
    ]