# -*- coding: utf-8 -*-

from django.conf.urls import url

from front import views

app_name = 'front'
urlpatterns = [
  
    url(r'^$', views.index, name = 'index'),
    url(r'^login/$', views.the_login, name = 'login'),
    url(r'^consulta/$', views.consulta, name = 'consulta'),
    url(r'^lista/$', views.lista, name = 'lista'),
    url(r'^licencia/$', views.licencia, name = 'licencia'),

]
