# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Persona(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    dni = models.CharField(max_length=8, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    donacion = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='fotos', max_length=100)
    firma = models.ImageField(upload_to='firmas', max_length=100)

    def __str__(self):
        return '%s %s' % (self.nombres,self.apellidos)

class Autoridad(models.Model):
    nombre_autoridad = models.CharField(max_length=255)
    fecha_inicio_autoridad = models.DateField()
    fecha_inicio_autoridad = models.DateField()
    firma_autoridad = models.ImageField(upload_to='firmas_autoridad', max_length=100)

    class Meta:
        verbose_name_plural='Autoridades'

    def __str__(self):
        return  self.nombre_autoridad
class Licencia(models.Model):
    CLASES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )
    CATEGORIAS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    ESTADO = (
        ('Activo', 'Activo'),
        ('Vencido', 'Vencido'),
        ('Sancionado', 'Sancionado'),
    )
    persona = models.ForeignKey(Persona)
    autoridad = models.ForeignKey(Autoridad)
    clase = models.CharField(max_length=1, choices=CLASES, default='A')
    categoria = models.CharField(max_length=1, choices=CATEGORIAS, default='1')
    numero_licencia = models.IntegerField()
    fecha_expedicion = models.DateField()
    fecha_revalidacion = models.DateField()
    restricciones = models.TextField(blank=True, null=True, default='Ninguno')
    estado = models.CharField(max_length=10, choices=ESTADO, default='Activo')

import datetime
class Sancion(models.Model):
    SANCIONES = (
        ('Innabilitacion', 'Innabilitacion'),
        ('Suspencion', 'Suspencion'),
        ('Sentencia', 'Sentencia'),
        ('Multa', 'Multa'),
    )
    persona = models.ForeignKey(Persona)
    fecha_infracion = models.DateField()
    numero_papeleta = models.IntegerField()
    entidad = models.CharField(max_length=255)
    distrito = models.CharField(max_length=255)
    infracion = models.CharField(max_length=255)
    grado_alcohol = models.CharField(max_length=255)
    retencion = models.CharField(max_length=15, choices=SANCIONES, default='Multa')
    observacion = models.CharField(max_length=255, default='Ninguna')
    fecha_inicio = models.DateField(default=datetime.datetime.now, blank=True)
    fecha_fin = models.DateField(default=datetime.datetime.now, blank=True)
    carnet_policial = models.IntegerField()

    class Meta:
        verbose_name_plural='Sanciones'

