# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from base.models import Licencia
from base.models import Persona, Sancion
from base.forms import PersonaForm, LicenciaForm, SancionForm

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
def personas(request):
    personas = Persona.objects.all()
    return render(request, 'front/personas.html', {'personas': personas})

@login_required
def licencia(request, id=None):
    l=None
    if id is not None:
        l=Licencia.objects.get(id=id)
    if request.method == 'POST':
        if l is None:
            form = LicenciaForm(request.POST)
        else:
            form = LicenciaForm(request.POST,instance=l)
        if form.is_valid():
            licencia = form.save(commit=False)
            persona = request.POST.get('persona')
            persona = Persona.objects.get(id = persona)
            licencia.persona = persona
            licencia.save()
            if l is None:
                messages.warning(request, 'Se ha creado una licencia.')
            else:
                messages.warning(request, 'Se ha Actualizado una licencia.')
            return HttpResponseRedirect(reverse('front:consulta'))
        else:
            return render(request, 'front/licencia.html', {'form': form})
    else:
        if l is None:
            form = LicenciaForm()   
        else:
            form = LicenciaForm(instance=l)
        return render(request, 'front/licencia.html', {'form': form})

@login_required
def persona(request, id=None):
    p=None
    if id is not None:
        p=Persona.objects.get(id=id)
    if request.method == 'POST':
        if p is None:
            form = PersonaForm(request.POST, request.FILES)
        else:
            form = PersonaForm(request.POST,request.FILES,instance=p)
        if form.is_valid():
            persona = form.save(commit=False)
            persona.save()
            if p is None:
                messages.warning(request, 'Se ha creado una Persona.')
            else:
                messages.warning(request, 'Se ha Actualizado una Persona.')
            return HttpResponseRedirect(reverse('front:personas'))
        else:
            return render(request, 'front/persona.html', {'form': form})
    else:
        if p is None:
            form = PersonaForm()   
        else:
            form = PersonaForm(instance=p)
        return render(request, 'front/persona.html', {'form': form})

@login_required
def sancion_persona(request, id_persona, id):
    persona=Persona.objects.get(id=id_persona)
    s = None
    if id != '0':
        s = Sancion.objects.get(id=id)
    if s is None:
        form = SancionForm()
    else:
        form = SancionForm(instance=s)
    if request.method == 'POST':
        if s is None:
            form = SancionForm(request.POST)
        else:
            form = SancionForm(request.POST, instance=s)

        if form.is_valid():
            sancion = form.save(commit=False)
            sancion.persona=persona
            sancion.save()
            if s is None:
                messages.warning(request, 'Se ha creado una sanción para %s.' % persona)
            else:
                messages.warning(request, 'Se ha actualizado una sanción para %s.' % persona)
            return HttpResponseRedirect(reverse('front:personas'))
        else:
            return render(request, 'front/sanciones.html', {'form': form, 'persona':persona})
    else:
        return render(request, 'front/sancion.html', {'form': form, 'persona':persona})

@login_required
def sanciones_persona(request, persona_id):
    persona=Persona.objects.get(id=persona_id)
    sanciones=Sancion.objects.filter(persona=persona)
    return render(request, 'front/lista-sanciones.html', {'sanciones': sanciones, 'persona':persona})
