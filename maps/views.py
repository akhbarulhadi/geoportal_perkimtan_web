from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GarisPantai, KawasanKumuh, JalanLingkungan
from django.contrib.gis.serializers import geojson

# Create your views here.

@login_required(login_url='/login')
def index(request):

    isi = {
		'page_title': 'Peta',
    }
    return render(request,'maps/index.html', isi)

@login_required(login_url='/login')
def garis_pantai_view(request):
    garis_pantai = geojson.Serializer().serialize(GarisPantai.objects.all())

    isi = {
        'garis_pantai': garis_pantai,

    }

    return render(request, 'maps/garis_pantai.html', isi)