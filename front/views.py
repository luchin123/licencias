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

from front.utils import crear_enlace, timestamp_a_fecha

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
            'DNI', 'Persona', 'Autoridad', 'Clase', 'Categoria', 'Nro', 'Fecha Exp', 'Fecha Rev', 'Acciones'
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

    if 'column[8]' in cols:
        signo = '' if request.GET.get('column[8]') == '0' else '-'
        licencias = licencias.order_by('%sfecha_revalidacion' % signo)

    total_rows = licencias.count()

    licencias = licencias[limit:offset]

    rows = []
    for licencia in licencias:

        links = crear_enlace(reverse('front:licencia', args=[licencia.id]), 'success', 'Ver o Editar', 'edit')

        obj = OrderedDict({
            '0': licencia.persona.dni,
            '1': licencia.persona.apellidos + ' ' + licencia.persona.nombres,
            '2': licencia.autoridad.nombre_autoridad,
            '3': licencia.clase,
            '4': licencia.categoria,
            '5': licencia.numero_licencia,
            '6': licencia.fecha_expedicion.strftime('%d/%b/%Y'),
            '7': licencia.fecha_revalidacion.strftime('%d/%b/%Y'),
            '8': links,
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
            'Nombres', 'Apellidos', 'Fecha Nacimiento', 'Direccion', 'Donacion', 'Foto', 'Acciones'
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
        personas = personas.filter(donacion = request.GET.get('filter[4]'))

    if 'filter[5]' in filters:
        personas = personas.filter(foto = request.GET.get('filter[5]'))

    

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

    if 'column[5]' in cols:
        signo = '' if request.GET.get('column[5]') == '0' else '-'
        personas = personas.order_by('%sfoto' % signo)


    total_rows = personas.count()

    personas = personas[limit:offset]

    rows = []
    for persona in personas:

        links = crear_enlace(reverse('front:persona', args=[persona.id]), 'success', 'Ver o Editar', 'edit')
        links = crear_enlace(reverse('front:persona', args=[persona.id]), 'success', 'Ver o Editar', 'edit')

        obj = OrderedDict({
            '0': persona.nombres,
            '1': persona.apellidos,
            '2': persona.fecha_nacimiento.strftime('%d/%b/%Y'),
            '3': persona.direccion,
            '4': persona.Donacion,
            '5': persona.foto,
            '6': links,
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
            if s is None:
                messages.warning(request, 'Se ha creado una sanción para %s.' % persona)
            else:
                messages.warning(request, 'Se ha actualizado una sanción para %s.' % persona)
            return HttpResponseRedirect(reverse('front:personas'))
        else:
            return render(request, 'front/sancion.html', {'form': form, 'persona':persona})
    else:
        return render(request, 'front/sancion.html', {'form': form, 'persona':persona})

"""
@login_required
def sanciones_persona(request, persona_id):
    persona=Persona.objects.get(id=persona_id)
    sanciones=Sancion.objects.filter(persona=persona)
    return render(request, 'front/lista-sanciones.html', {'sanciones': sanciones, 'persona':persona})
"""
@login_required
def sanciones_persona(request, persona_id):
    persona=Persona.objects.get(id=persona_id)
    sanciones=Sancion.objects.filter(persona=persona)
    return render(request, 'front/sanciones-lista.html', {'sanciones': sanciones, 'persona':persona})

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
            'Persona', 'Fecha de Infraccion', 'Número Papeleta', 'Entidad', 'Distrito', 'Infracion','Grado Alcohol','Retencion','Carnet Policial', 'Acciones'
        ]

    }

    sanciones = Sancion.objects.all().order_by('-pk')

    if 'filter[0]' in filters:
        sanciones = sanciones.filter(persona__contains = request.GET.get('filter[0]'))
    if 'filter[1]' in filters:
        str_fecha = request.GET.get('filter[1]')
        if str_fecha[:2] == '<=':
            fecha = str_fecha[2:12]
            sanciones = sanciones.distinct().filter(fecha_infracion__lte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        elif str_fecha[:2] == '>=':
            fecha = str_fecha[2:12]
            sanciones = sanciones.distinct().filter(fecha_infracion__gte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        else:
            inicial = timestamp_a_fecha(str_fecha[:10], '%Y-%m-%d')
            final = timestamp_a_fecha(str_fecha[-13:][:10], '%Y-%m-%d')
            sanciones = sanciones.distinct().filter(fecha_infracion__range = (inicial, final))

    if 'filter[2]' in filters:
        sanciones = sanciones.filter(numero_papeleta__icontains = request.GET.get('filter[2]'))

    if 'filter[3]' in filters:
        sanciones = sanciones.filter(entidad__icontains = request.GET.get('filter[3]'))

    if 'filter[4]' in filters:
        sanciones = sanciones.filter(distrito__icontains = request.GET.get('filter[4]'))

    if 'filter[5]' in filters:
        sanciones = sanciones.filter(infracion__icontains = request.GET.get('filter[5]'))

    if 'filter[6]' in filters:
        sanciones = sanciones.filter(grado_alcohol = request.GET.get('filter[6]'))

    if 'filter[7]' in filters:
        sanciones = sanciones.filter(retencion = request.GET.get('filter[7]'))

    if 'filter[8]' in filters:
        sanciones = sanciones.filter(carnet_policial = request.GET.get('filter[8]'))

    

    if 'column[0]' in cols:
        signo = '' if request.GET.get('column[0]') == '0' else '-'
        sanciones = sanciones.order_by('%spersona' % signo)

    if 'column[1]' in cols:
        signo = '' if request.GET.get('column[1]') == '0' else '-'
        sanciones = sanciones.order_by('%sfecha_infraccionn' % signo)

    if 'column[2]' in cols:
        signo = '' if request.GET.get('column[2]') == '0' else '-'
        sanciones = sanciones.order_by('%snumero_papeleta' % signo)

    if 'column[3]' in cols:
        signo = '' if request.GET.get('column[3]') == '0' else '-'
        sanciones = sanciones.order_by('%sentidad' % signo)

    if 'column[4]' in cols:
        signo = '' if request.GET.get('column[4]') == '0' else '-'
        sanciones = sanciones.order_by('%sdistrito' % signo)

    if 'column[5]' in cols:
        signo = '' if request.GET.get('column[5]') == '0' else '-'
        sanciones = sanciones.order_by('%sinfraccion' % signo)
    if 'column[6]' in cols:
        signo = '' if request.GET.get('column[6]') == '0' else '-'
        sanciones = sanciones.order_by('%sgrado_alcohol' % signo)
    if 'column[7]' in cols:
        signo = '' if request.GET.get('column[7]') == '0' else '-'
        sanciones = sanciones.order_by('%sretencion' % signo)
    if 'column[8]' in cols:
        signo = '' if request.GET.get('column[8]') == '0' else '-'
        sanciones = sanciones.order_by('%scarnet_policial' % signo)


    total_rows = sanciones.count()

    sanciones = sanciones[limit:offset]

    rows = []
    for sancion in sanciones:

        links = crear_enlace(reverse('front:sanciones_persona', args=[sancion.id]), 'success', 'Ver o Editar', 'edit')

        obj = OrderedDict({
            '0': sancion.persona.nombres,
            '1': sancion.fecha_infracion.strftime('%d/%b/%Y'),
            '2': sancion.numero_papeleta,
            '3': sancion.entidad,
            '4': sancion.distrito,
            '5': sancion.infracion,
            '6': sancion.grado_alcohol,
            '7': sancion.retencion,
            '8': sancion.carnet_policial,
            '9': links,
        })
        rows.append(obj)

    data['rows'] = rows
    data['total_rows'] = total_rows

    return HttpResponse(json.dumps(data), content_type = "application/json")
