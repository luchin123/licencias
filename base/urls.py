# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'personas', views.PersonaViewSet)

app_name = 'base'
urlpatterns = [

    url(r'^api/base/', include(router.urls)),
    url(r'^api/base/persona/filter/$', views.PersonaFilterViewSet.as_view()),

]
