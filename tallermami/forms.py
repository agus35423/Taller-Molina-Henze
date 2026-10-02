from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Turno, Trabajo


# ==========================================================
# FORMULARIO PARA SOLICITAR TURNO
# ==========================================================

class SolicitarTurnoForm(forms.ModelForm):

    nombre = forms.CharField(
        max_length=100,
        label="Nombre"
    )

    apellido = forms.CharField(
        max_length=100,
        label="Apellido"
    )

    email = forms.EmailField(
        label="Correo electrónico"
    )

    telefono = forms.CharField(
        max_length=30,
        label="Teléfono"
    )

    class Meta:
        model = Turno

        fields = [
            "vehiculo",
            "patente",
            "servicio",
            "fecha_turno",
            "observaciones",
        ]

        widgets = {
            "vehiculo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Toyota Corolla 2020"
                }
            ),

            "patente": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: AB123CD",
                    "style": "text-transform: uppercase;"
                }
            ),

            "servicio": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "fecha_turno": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                }
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Contanos qué problema tiene el vehículo..."
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["servicio"].queryset = Trabajo.objects.all()

        self.fields["nombre"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Tu nombre"
        })

        self.fields["apellido"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Tu apellido"
        })

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "correo@ejemplo.com"
        })

        self.fields["telefono"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "351..."
        })

    def clean_patente(self):

        patente = self.cleaned_data["patente"]

        return patente.upper().replace(" ", "").replace("-", "")

    def clean_fecha_turno(self):

        fecha = self.cleaned_data.get("fecha_turno")

        if not fecha:
            return fecha

        cantidad_turnos = Turno.objects.filter(
            fecha_turno__date=fecha.date()
        ).count()

        if self.instance and self.instance.pk:
            cantidad_turnos -= 1

        if cantidad_turnos >= 3:

            raise forms.ValidationError(
                "Esta fecha ya está completa. "
                "Ya hay 3 turnos asignados. "
                "Por favor, seleccioná otra fecha."
            )

        return fecha


# ==========================================================
# FORMULARIO DE REGISTRO
# ==========================================================

class RegistroForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Correo electrónico"
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                "class": "form-control"
            })