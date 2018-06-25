# -*- coding: utf-8 -*-

from django.conf.urls import url

from front import views

app_name = 'front'
urlpatterns = [
  
    url(r'^$', views.index, name = 'index'),
    url(r'^login/$', views.the_login, name = 'login'),
    url(r'^consulta/$', views.consulta, name = 'consulta'),
    url(r'^consultas/json/$', views.consulta_json, name = 'consulta_json'),
    url(r'^licencia/$', views.licencia, name = 'licencia'),
    url(r'^licencia/(?P<id>.*)$', views.licencia, name = 'licencia'),
    url(r'^personas/$', views.personas, name = 'personas'),
    url(r'^personas/json/$', views.personas_json, name = 'personas_json'),
    url(r'^persona/$', views.persona, name = 'persona'),
    url(r'^persona/(?P<id>.*)$', views.persona, name = 'persona'),
    url(r'^sancion/(?P<id_persona>.*)/(?P<id>.*)$', views.sancion_persona, name = 'sancion_persona'),
    url(r'^sanciones/(?P<persona_id>.*)$', views.sanciones_persona, name = 'sanciones_persona'),

]
