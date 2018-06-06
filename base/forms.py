# -*- coding: utf-8 -*-

from django.forms import ModelForm, TextInput, Select, Textarea, DateField, CheckboxInput, FileInput

from models import Persona, Licencia, Sancion
from django.conf import settings

class PersonaForm(ModelForm):
    fecha_nacimiento = DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=TextInput(attrs={
            'class': 'form-control datepicker',
        })
    )
    class Meta:
        model = Persona
        fields = '__all__'
        widgets = {
            'nombres': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres',
            }),
            'apellidos': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos',
            }),
            'dni': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'DNI',
            }),
            'direccion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Direccion',
            }),
            'donacion': CheckboxInput(attrs={
                'class': 'form-check-input',
                'placeholder': 'Donacion',
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

class SancionForm(ModelForm):
    fecha_infracion = DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=TextInput(attrs={
            'class': 'form-control datepicker',
        })
    )
    class Meta:
        model = Sancion
        exclude = ('persona',)
        widgets = {
            'persona': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres',
            }),
            'numero_papeleta': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numero Papeleta',
            }),
            'entidad': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entidad',
            }),
            'distrito': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Distrito',
            }),
            'infracion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'infraccion',
            }),
            'grado_alcohol': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Grado de Alcohol',
            }),
            'carnet_policial': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
          
          
          
          
        }