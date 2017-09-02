# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from . import views		# Import views relative (to last import)
from . import views

urlpatterns = [url(r'^$', views.index, name='index')]		# index ist der namespace. Beim Aufruf der webapp durch einen Webserver wird webapp.views.index (HTML Seite, welche Hey anzeigt) zurueckgegeben.Als Name wird index im Browser angezeigt

