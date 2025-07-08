from django.contrib.gis.db import models

# Create your models here.
    
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

