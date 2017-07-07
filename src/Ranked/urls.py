"""Ranked URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# Django Imports
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Project Imports
import src.api.urls as api_urls
from src.profile.models import Profile

admin.site.register(Profile, UserAdmin)
admin.autodiscover()

urlpatterns = [
    url(r'^api/v1/', include(api_urls)),
    url(r'^josh/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns = [
        url(r'^silk/', include('silk.urls', namespace='silk'))
    ] + urlpatterns
