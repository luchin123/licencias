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

from front.utils import crear_enlace, timestamp_a_fecha, sancionar_persona

from collections import OrderedDict
import json

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

"""
def consulta(request):
    licencias = Licencia.objects.all()
    return render(request, 'front/consulta.html',{'licencias': licencias})
"""
def consulta(request):
    return render(request, 'front/consulta-lista.html')

def consulta_json(request):
    filters = []
    cols = []
    for k in request.GET:
        if 'filter[' in k:
            filters.append(k)
        if 'column[' in k:
            cols.append(k)

    size = int(request.GET.get('size'))
    page = int(request.GET.get('page'))

    limit = page * size
    offset = limit + size

    data = {
        'headers': [
            'DNI', 'Persona', 'Autoridad', 'Clase', 'Categoria', 'Nro', 'Fecha Exp', 'Fecha Rev','Estado', 'Acciones'
        ]

    }

    licencias = Licencia.objects.all().order_by('-pk')

    if 'filter[0]' in filters:
        licencias = licencias.filter(persona__dni__contains = request.GET.get('filter[0]'))

    if 'filter[1]' in filters:
        licencias = licencias.filter(persona__nombres__icontains = request.GET.get('filter[1]')) | licencias.filter(persona__apellidos__icontains = request.GET.get('filter[1]'))

    if 'filter[2]' in filters:
        licencias = licencias.filter(autoridad__nombre_autoridad__icontains = request.GET.get('filter[2]'))

    if 'filter[3]' in filters:
        licencias = licencias.filter(clase__icontains = request.GET.get('filter[3]'))

    if 'filter[4]' in filters:
        licencias = licencias.filter(categoria = request.GET.get('filter[4]'))

    if 'filter[5]' in filters:
        licencias = licencias.filter(numero_licencia = request.GET.get('filter[5]'))

    if 'filter[6]' in filters:
        str_fecha = request.GET.get('filter[6]')
        if str_fecha[:2] == '<=':
            fecha = str_fecha[2:12]
            licencias = licencias.distinct().filter(fecha_expedicion__lte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        elif str_fecha[:2] == '>=':
            fecha = str_fecha[2:12]
            licencias = licencias.distinct().filter(fecha_expedicion__gte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        else:
            inicial = timestamp_a_fecha(str_fecha[:10], '%Y-%m-%d')
            final = timestamp_a_fecha(str_fecha[-13:][:10], '%Y-%m-%d')
            licencias = licencias.distinct().filter(fecha_expedicion__range = (inicial, final))

    if 'filter[7]' in filters:
        str_fecha = request.GET.get('filter[7]')
        if str_fecha[:2] == '<=':
            fecha = str_fecha[2:12]
            licencias = licencias.distinct().filter(fecha_revalidacion__lte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        elif str_fecha[:2] == '>=':
            fecha = str_fecha[2:12]
            licencias = licencias.distinct().filter(fecha_revalidacion__gte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        else:
            inicial = timestamp_a_fecha(str_fecha[:10], '%Y-%m-%d')
            final = timestamp_a_fecha(str_fecha[-13:][:10], '%Y-%m-%d')
            licencias = licencias.distinct().filter(fecha_revalidacion__range = (inicial, final))
    if 'filter[8]' in filters:
        licencias = licencias.filter(estado = request.GET.get('filter[8]'))

    if 'column[0]' in cols:
        signo = '' if request.GET.get('column[0]') == '0' else '-'
        licencias = licencias.order_by('%dni' % signo)

    if 'column[1]' in cols:
        signo = '' if request.GET.get('column[1]') == '0' else '-'
        licencias = licencias.order_by('%spersona__apellido' % signo)

    if 'column[2]' in cols:
        signo = '' if request.GET.get('column[2]') == '0' else '-'
        licencias = licencias.order_by('%sautoridad__nombre_autoridad' % signo)

    if 'column[3]' in cols:
        signo = '' if request.GET.get('column[3]') == '0' else '-'
        licencias = licencias.order_by('%sclase' % signo)

    if 'column[4]' in cols:
        signo = '' if request.GET.get('column[4]') == '0' else '-'
        licencias = licencias.order_by('%scategoria' % signo)

    if 'column[5]' in cols:
        signo = '' if request.GET.get('column[5]') == '0' else '-'
        licencias = licencias.order_by('%snumero' % signo)

    if 'column[6]' in cols:
        signo = '' if request.GET.get('column[6]') == '0' else '-'
        licencias = licencias.order_by('%sfecha_expedicion' % signo)

    if 'column[7]' in cols:
        signo = '' if request.GET.get('column[7]') == '0' else '-'
        licencias = licencias.order_by('%sfecha_revalidacion' % signo)
    if 'column[8]' in cols:
        signo = '' if request.GET.get('column[8]') == '0' else '-'
        licencias = licencias.order_by('%sestado' % signo)

    total_rows = licencias.count()

    licencias = licencias[limit:offset]

    rows = []
    for licencia in licencias:


        # Esto es para saber si el usuario está autenticado, sino no tiene porque imprimir la licencia ok
        if request.user.is_authenticated():
            links = crear_enlace(reverse('front:licencia', args=[licencia.id]), 'success', 'Ver o Editar', 'edit')
            links += crear_enlace(reverse('reporte:licencia_print', args=[licencia.id]), 'success', 'Imprimir', 'print')


        obj = OrderedDict({
            '0': licencia.persona.dni,
            '1': licencia.persona.apellidos + ' ' + licencia.persona.nombres,
            '2': licencia.autoridad.nombre_autoridad,
            '3': licencia.clase,
            '4': licencia.categoria,
            '5': licencia.numero_licencia,
            '6': licencia.fecha_expedicion.strftime('%d/%b/%Y'),
            '7': licencia.fecha_revalidacion.strftime('%d/%b/%Y'),
            '8': licencia.estado,
            '9': links,
        })
        rows.append(obj)

    data['rows'] = rows
    data['total_rows'] = total_rows

    return HttpResponse(json.dumps(data), content_type = "application/json")

@login_required
def index(request):
    return render(request, 'front/index.html')
"""
@login_required
def personas(request):
    personas = Persona.objects.all()
    return render(request, 'front/personas.html', {'personas': personas})
"""
@login_required
def personas(request):
    return render(request, 'front/personas-lista.html')

def personas_json(request):
    filters = []
    cols = []
    for k in request.GET:
        if 'filter[' in k:
            filters.append(k)
        if 'column[' in k:
            cols.append(k)

    size = int(request.GET.get('size'))
    page = int(request.GET.get('page'))

    limit = page * size
    offset = limit + size

    data = {
        'headers': [
            'Nombres', 'Apellidos', 'Fecha Nacimiento', 'Direccion', 'Donacion', 'Acciones'
        ]

    }

    personas = Persona.objects.all().order_by('-pk')

    if 'filter[0]' in filters:
        personas = personas.filter(nombres__contains = request.GET.get('filter[0]'))

    if 'filter[1]' in filters:
        personas = personas.filter(apellidos__icontains = request.GET.get('filter[1]'))
    if 'filter[2]' in filters:
        str_fecha = request.GET.get('filter[2]')
        if str_fecha[:2] == '<=':
            fecha = str_fecha[2:12]
            personas = personas.distinct().filter(fecha_nacimiento__lte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        elif str_fecha[:2] == '>=':
            fecha = str_fecha[2:12]
            personas = personas.distinct().filter(fecha_nacimiento__gte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        else:
            inicial = timestamp_a_fecha(str_fecha[:10], '%Y-%m-%d')
            final = timestamp_a_fecha(str_fecha[-13:][:10], '%Y-%m-%d')
            personas = personas.distinct().filter(fecha_nacimiento__range = (inicial, final))

    if 'filter[3]' in filters:
        personas = personas.filter(direccion__icontains = request.GET.get('filter[3]'))

    if 'filter[4]' in filters:
        d = request.GET.get('filter[4]') == 'Si'
        personas = personas.filter(donacion = d)

    

    if 'column[0]' in cols:
        signo = '' if request.GET.get('column[0]') == '0' else '-'
        personas = personas.order_by('%snombres' % signo)

    if 'column[1]' in cols:
        signo = '' if request.GET.get('column[1]') == '0' else '-'
        personas = personas.order_by('%sapellidos' % signo)

    if 'column[2]' in cols:
        signo = '' if request.GET.get('column[2]') == '0' else '-'
        personas = personas.order_by('%sfecha_nacimiento' % signo)

    if 'column[3]' in cols:
        signo = '' if request.GET.get('column[3]') == '0' else '-'
        personas = personas.order_by('%sdireccion' % signo)

    if 'column[4]' in cols:
        signo = '' if request.GET.get('column[4]') == '0' else '-'
        personas = personas.order_by('%sdonacion' % signo)


    total_rows = personas.count()

    personas = personas[limit:offset]

    rows = []
    for persona in personas:

        links = crear_enlace(reverse('front:persona', args=[persona.id]), 'success', 'Ver o Editar', 'edit')
        links += crear_enlace(reverse('front:sanciones_persona', args=[persona.id]), 'danger', 'Ver sanciones', 'ban')

        obj = OrderedDict({
            '0': persona.nombres,
            '1': persona.apellidos,
            '2': persona.fecha_nacimiento.strftime('%d/%b/%Y'),
            '3': persona.direccion,
            '4': 'Si' if persona.donacion else 'No',
            '5': links,
        })
        rows.append(obj)

    data['rows'] = rows
    data['total_rows'] = total_rows

    return HttpResponse(json.dumps(data), content_type = "application/json")

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
            sancionar_persona(persona, sancion.retencion)
            if s is None:
                messages.warning(request, 'Se ha creado una sanción para %s.' % persona)
            else:
                messages.warning(request, 'Se ha actualizado una sanción para %s.' % persona)
            return HttpResponseRedirect(reverse('front:personas'))
        else:
            return render(request, 'front/sancion.html', {'form': form, 'persona':persona})
    else:
        return render(request, 'front/sancion.html', {'form': form, 'persona':persona})


@login_required
def sanciones_persona(request, persona_id):
    persona=Persona.objects.get(id=persona_id)
    return render(request, 'front/lista-sanciones.html', {'persona':persona})

