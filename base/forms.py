# -*- coding: utf-8 -*-

from django.forms import ModelForm, TextInput, Select, Textarea, DateField

from models import Persona, Licencia
from django.conf import settings

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        exclude = '__all__'
        widgets = {
            'nombres': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres',
            }),
        }


class LicenciaForm(ModelForm):
    fecha_expedicion = DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=TextInput(attrs={
            'class': 'form-control datepicker',
        })
    )

    fecha_revalidacion = DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=TextInput(attrs={
            'class': 'form-control datepicker',
        })
    )

    class Meta:
        model = Licencia
        exclude = ('persona',)
        widgets = {
            'autoridad': Select(attrs={
                'class': 'form-control',
            }),
            'clase': Select(attrs={
                'class': 'form-control',
            }),
            'categoria': Select(attrs={
                'class': 'form-control',
            }),
            'numero_licencia': TextInput(attrs={
                'class': 'form-control',
            }),
            'restricciones': Textarea(attrs={
                'class': 'form-control',
            }),
        }
