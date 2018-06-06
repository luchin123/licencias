# -*- coding: utf-8 -*-

from django.conf.urls import url

from front import views

app_name = 'front'
urlpatterns = [
  
    url(r'^$', views.index, name = 'index'),
    url(r'^login/$', views.the_login, name = 'login'),
    url(r'^consulta/$', views.consulta, name = 'consulta'),
    url(r'^licencia/$', views.licencia, name = 'licencia'),
    url(r'^licencia/(?P<id>.*)$', views.licencia, name = 'licencia'),
    url(r'^lista/$', views.lista, name = 'lista'),
    url(r'^persona/$', views.persona, name = 'persona'),
    url(r'^persona/(?P<id>.*)$', views.persona, name = 'persona'),
    url(r'^sancion/(?P<id_persona>.*)/(?P<id>.*)$', views.sancion, name = 'sancion'),
    url(r'^lista-sanciones/(?P<persona_id>.*)$', views.listaS, name = 'lista_sanciones'),

]
