# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from base.models import Licencia
from base.models import Persona
from base.forms import PersonaForm, LicenciaForm

def the_login(request):
    if(request.user.is_authenticated()):
        return HttpResponseRedirect(reverse('front:index'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('front:index'))
            else:
                messages.warning(request, 'El usuario no está activo.')
        else:
            messages.warning(request, 'Revise el usuario o la contraseña.')
        

    return render(request, 'front/login.html')

def consulta(request):
    licencias = Licencia.objects.all()
    return render(request, 'front/consulta.html',{'licencias': licencias})

@login_required
def index(request):
    return render(request, 'front/index.html')

@login_required
def lista(request):
    personas = Persona.objects.all()
    return render(request, 'front/lista.html', {'personas': personas})


@login_required
def licencia(request):
    if request.method == 'POST':
        form = LicenciaForm(request.POST)
        if form.is_valid():
            licencia = form.save(commit=False)
            persona = request.POST.get('persona')
            persona = Persona.objects.get(id = persona)
            licencia.persona = persona
            licencia.save()

            messages.warning(request, 'Se ha creado una licencia.')
            return HttpResponseRedirect(reverse('front:consulta'))
        else:
            return render(request, 'front/licencia.html', {'form': form})
    else:
        form = LicenciaForm()
        return render(request, 'front/licencia.html', {'form': form})
