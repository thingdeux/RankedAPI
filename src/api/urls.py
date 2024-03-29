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
from src.profile.viewsets import RegisterViewSet, ProfileViewSet
from src.profile.views import me, AvatarUploadView
from src.video.views import GenerateUploadView, sns_error, sns_success
from src.video.viewsets import VideoViewSet, VideoTopView
from src.categorization.viewsets import CategoryViewSet
from django.conf import settings
from .views import search

router = routers.DefaultRouter()
router.register(r'users/register', RegisterViewSet)
router.register(r'users', ProfileViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    url(r'^users/auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^users/me/$', me),
    url(r'^users/me/avatar/$', AvatarUploadView.as_view()),
    url(r'^videos/processing/done/$', sns_success),
    url(r'^videos/processing/error/$', sns_error),
    url(r'^videos/upload/$', GenerateUploadView.as_view()),
    url(r'^videos/top/$', VideoTopView.as_view()),
    url(r'^search/explore/$', search, {'route': 'explore'}),
    url(r'^search/ranked10/$', search, {'route': 'ranked10'}),
    url(r'^search/trending/$', search, {'route': 'trending'}),
    url(r'^search/trendsetters/$', search, {'route': 'trendsetters'}),
    url(r'^search/$', search, {'route': 'base'}),
    url(r'^', include(router.urls)),
]
