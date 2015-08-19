"""fantasy_map URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from fantasy_map.main import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="main/index.html")),
    url(r'^biomes_data.json$', views.biomes_data, name="biomes_data"),
    url(r'^regions_data.json$', views.regions_data, name="regions_data"),
    url(r'^cities_data.json$', views.cities_data, name="cities_data"),
    url(r'^admin/', include(admin.site.urls)),
]
