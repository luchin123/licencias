# -*- coding: utf-8 -*-

from django.conf.urls import url

from reporte import views

app_name = 'reporte'
urlpatterns = [
  
    url(r'^imprimir/licencia/(?P<id>.*)$', views.licencia_print, name = 'licencia_print'),

]
