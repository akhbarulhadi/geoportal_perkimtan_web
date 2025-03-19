from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import GarisPantai, KawasanKumuh, JalanLingkungan

class CustomGeoAdmin(GISModelAdmin):
    default_lon = 104.0305  # Dalam EPSG:4326
    default_lat = 1.1049
    default_zoom = 12
    map_srid = 4326  # Paksa pakai 4326


@admin.register(GarisPantai)
class GarisPantaiAdmin(CustomGeoAdmin):
    list_display = ('nama', 'created_at')

@admin.register(KawasanKumuh)
class KawasanKumuhAdmin(CustomGeoAdmin):
    list_display = ('nama', 'created_at')

@admin.register(JalanLingkungan)
class JalanLingkunganAdmin(CustomGeoAdmin):
    list_display = ('nama', 'created_at')
