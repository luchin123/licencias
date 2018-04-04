# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from base.models import Persona
from base.forms import PersonaForm

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
    return render(request, 'front/consulta.html')

@login_required
def index(request):
    return render(request, 'front/index.html')

@login_required
def lista(request):
    personas = Persona.objects.all()
    return render(request, 'front/lista.html', {'personas': personas})

