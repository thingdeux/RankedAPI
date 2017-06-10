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
from django.conf.urls import url, include
from rest_framework import routers
from src.profile.viewsets import me, RegisterViewSet

router = routers.DefaultRouter()
router.register(r'users/register', RegisterViewSet)

urlpatterns = [
    url(r'^users/auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^users/me/', me),
    url(r'^', include(router.urls)),
]