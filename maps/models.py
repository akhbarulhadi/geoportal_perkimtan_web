from django.contrib.gis.db import models

# Create your models here.

class GarisPantai(models.Model):
    nama = models.CharField(max_length=255)
    geom = models.LineStringField(srid=4326)  # Garis pantai menggunakan LineString
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

class KawasanKumuh(models.Model):
    nama = models.CharField(max_length=255)
    geom = models.PolygonField(srid=4326)  # Kawasan kumuh sebagai Polygon
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

class JalanLingkungan(models.Model):
    nama = models.CharField(max_length=255)
    geom = models.LineStringField(srid=4326)  # Jalan lingkungan sebagai LineString
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama
