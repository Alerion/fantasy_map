from django.core.serializers import serialize
from django.http import HttpResponse

from .models import Biome, Region, City


def biomes_data(request):
    output = serialize('geojson', Biome.objects.all(),
                       geometry_field='geom', fields=('biome', 'geom'))
    return HttpResponse(output, content_type='text/json')


def regions_data(request):
    output = serialize('geojson', Region.objects.all(),
                       geometry_field='geom', fields=('name', 'geom'))
    return HttpResponse(output, content_type='text/json')


def cities_data(request):
    output = serialize('geojson', City.objects.all(),
                       geometry_field='coords', fields=('name', 'coords'))
    return HttpResponse(output, content_type='text/json')
