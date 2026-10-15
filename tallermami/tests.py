from django.test import TestCase
from django.contrib.auth.models import User


class PanelJefeTests(TestCase):

    def test_panel_jefe_redirige_a_login_si_no_hay_sesion(self):
        respuesta = self.client.get("/jefe/")

        self.assertRedirects(
            respuesta,
            "/login/?next=/jefe/"
        )

    def test_panel_jefe_rechaza_usuarios_no_superusuarios(self):
        usuario = User.objects.create_user(
            username="cliente",
            password="contrasena-segura"
        )
        self.client.force_login(usuario)

        respuesta = self.client.get("/jefe/")

        self.assertEqual(respuesta.status_code, 403)

    def test_panel_jefe_muestra_turnos_a_superusuario(self):
        superusuario = User.objects.create_superuser(
            username="jefe",
            email="jefe@example.com",
            password="contrasena-segura"
        )
        self.client.force_login(superusuario)

        respuesta = self.client.get("/jefe/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Panel del jefe")
        self.assertContains(respuesta, "Total de turnos")
