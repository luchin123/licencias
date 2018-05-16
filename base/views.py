# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .serializers import PersonaSerializer
from rest_framework import viewsets, generics
from base.models import Persona

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

class PersonaFilterViewSet(generics.ListAPIView):
    serializer_class = PersonaSerializer

    def get_queryset(self):
        queryset = Persona.objects.all()
        term = self.request.query_params.get('term', None)

        if term is not None:
            queryset = queryset.filter(nombres__istartswith = term) | queryset.filter(apellidos__istartswith = term) | queryset.filter(dni__startswith = term)
        return queryset
