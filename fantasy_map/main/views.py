from django.core.serializers import serialize
from django.http import HttpResponse

from .models import Biome


def biomes_data(request):
    output = serialize('geojson', Biome.objects.all(),
                       geometry_field='geom', fields=('biome', 'geom'))
    return HttpResponse(output, content_type='text/json')
