# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from base.models import Persona, Licencia, Autoridad, Sancion

class PersonaAdmin(admin.ModelAdmin):
	list_display = ('nombres', 'apellidos')

admin.site.register(Persona, PersonaAdmin)
admin.site.register(Licencia)
admin.site.register(Autoridad)
admin.site.register(Sancion)
