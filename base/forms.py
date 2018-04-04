# -*- coding: utf-8 -*-

from django.forms import ModelForm, TextInput

from models import Persona

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
