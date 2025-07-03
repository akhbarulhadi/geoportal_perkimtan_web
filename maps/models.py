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

class Maps(models.Model):
    id_maps = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)
    photo_maps = models.ImageField(upload_to='maps_photo/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama
    
class FieldMaps(models.Model):
    id_field_maps = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)
    id_maps = models.ForeignKey(Maps, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama
    
class DataMaps(models.Model):
    id_data_maps = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)
    id_field_maps = models.ForeignKey(FieldMaps, on_delete=models.CASCADE)
    geom = models.GeometryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama
    
class GeoDataset(models.Model):
    nama_dataset = models.CharField(max_length=100)
    geometry = models.GeometryField(srid=4326)   # WGS‑84 → cocok utk Leaflet
    kategori = models.CharField(max_length=100)
    properties = models.JSONField()
    pending = models.BooleanField(default=True)

    def __str__(self):
        try:
            return f"{self.rumah.nama_pemilik} (id={self.id} {self.kategori})"
        except Exception:
            return f"(id={self.id} {self.kategori})"

class UploadProgress(models.Model):
    task_id = models.CharField(max_length=100, unique=True)
    progress = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default="processing")  # or 'done', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

