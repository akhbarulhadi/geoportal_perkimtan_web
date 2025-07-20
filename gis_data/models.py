from django.contrib.gis.db import models
from maps.models import GeoDataset
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
    
class Kecamatan(models.Model):
    id_kecamatan = models.AutoField(primary_key=True)
    kecamatan = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.kecamatan)
    
class Kelurahan(models.Model):
    id_kelurahan = models.AutoField(primary_key=True)
    kelurahan = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.kelurahan)

class Perumahan(models.Model):
    id_perumahan = models.AutoField(primary_key=True)
    nama_perumahan = models.CharField(max_length=255)
    photo_perumahan = models.ImageField(upload_to='perumahan_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    alamat_lengkap_perumahan = models.CharField(max_length=255)
    perumahan_subsidi = models.BooleanField(default=False)
    lokasi_perumahan = models.GeometryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.nama_perumahan)

class Rumah(models.Model):
    STATUS_RUMAH_CHOICES = [
        ('RUMAH_LAYAK_HUNI', 'Rumah Layak Huni'),
        ('RUMAH_TIDAK_LAYAK_HUNI', 'Rumah Tidak Layak Huni'),
    ]
    STATUS_LUAS_CHOICES = [
        ('LUAS_RUMAH_CUKUP', 'Luas Rumah Cukup'),
        ('LUAS_RUMAH_KURANG', 'Luas Rumah Kurang'),
    ]

    id_rumah = models.AutoField(primary_key=True)
    nama_pemilik = models.CharField(max_length=255, null=True, blank=True)
    alamat_rumah = models.CharField(max_length=255, null=True, blank=True)
    rumah_sewa = models.BooleanField(default=False)
    jumlah_kk = models.IntegerField(null=True, blank=True)
    nilai_keselamatan = models.IntegerField(null=True, blank=True)
    nilai_kesehatan = models.IntegerField(null=True, blank=True)
    nilai_komponen = models.IntegerField(null=True, blank=True)
    status_rumah = models.CharField(max_length=30, choices=STATUS_RUMAH_CHOICES, null=True, blank=True)
    status_luas = models.CharField(max_length=30, choices=STATUS_LUAS_CHOICES, null=True, blank=True)
    geo = models.OneToOneField(GeoDataset, on_delete=models.CASCADE)
    nama_perumahan = models.ForeignKey(Perumahan, on_delete=models.CASCADE, null=True, blank=True)
    photo_rumah = models.ImageField(upload_to='rumah_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    dibuat_oleh_users = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.nama_pemilik)

class RumahSusun(models.Model):
    id_rumah_susun = models.AutoField(primary_key=True)
    photo_rusun = models.ImageField(upload_to='rusun_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    alamat_rusun = models.CharField(max_length=255)
    nama_rusun = models.CharField(max_length=255)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    jumlah_kk = models.CharField(max_length=255)
    jumlah_unit_kamar = models.CharField(max_length=255)
    lokasi_rusun = models.GeometryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.nama_rusun)
  
class AddRequest(models.Model):
    photo_rumah = models.ImageField(upload_to='rumah_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    photo_perumahan = models.ImageField(upload_to='perumahan_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    geometry = models.GeometryField(srid=4326)
    data = models.JSONField(blank=True, null=True)
    dibuat_oleh = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dibuat_oleh_users = models.CharField(blank=True, null=True)
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    disetujui = models.BooleanField(default=False)
    ditolak = models.BooleanField(default=False)

class UpdateRequest(models.Model):
    id_rumah = models.ForeignKey(Rumah, on_delete=models.CASCADE, blank=True, null=True)
    photo_rumah = models.ImageField(upload_to='rumah_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    photo_perumahan = models.ImageField(upload_to='perumahan_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    geometry = models.GeometryField(srid=4326)
    data = models.JSONField(blank=True, null=True)
    dibuat_oleh = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dibuat_oleh_users = models.CharField(blank=True, null=True)
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    disetujui = models.BooleanField(default=False)
    ditolak = models.BooleanField(default=False)