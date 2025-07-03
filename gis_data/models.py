from django.contrib.gis.db import models
from maps.models import GeoDataset
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

# class DataSets(models.Model):
#     JENIS_CHOICES = [
#         ('PUBLIC', 'Public'),
#         ('PRIVATE', 'Private'),
#     ]
#     id_datasets = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=255)
#     abstract = models.CharField(max_length=255)
#     photo_datasets = models.ImageField(upload_to='datasets_photos/', null=True, blank=True)
#     status = models.CharField(max_length=30, choices=JENIS_CHOICES)
#     published = models.DateField(null=True, blank=True)  # Jika bisa belum ditentukan
#     last_modified = models.DateTimeField(auto_now=True)  # Otomatis diperbarui saat diupdate
#     created_at = models.DateTimeField(auto_now_add=True)  # Hanya saat pertama kali dibuat

#     def __str__(self):
#         return "{}".format(self.title)

    
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

    nama_pemilik = models.CharField(max_length=255)
    alamat_rumah = models.CharField(max_length=255)

    rumah_sewa = models.BooleanField(default=False)

    jumlah_kk = models.IntegerField()
    nilai_keselamatan = models.IntegerField(null=True, blank=True)
    nilai_kesehatan = models.IntegerField(null=True, blank=True)
    nilai_komponen = models.IntegerField(null=True, blank=True)

    status_rumah = models.CharField(max_length=30, choices=STATUS_RUMAH_CHOICES)
    status_luas = models.CharField(max_length=30, choices=STATUS_LUAS_CHOICES)

    geo = models.OneToOneField(GeoDataset, on_delete=models.CASCADE)

    nama_perumahan = models.ForeignKey(Perumahan, on_delete=models.CASCADE)
    photo_rumah = models.ImageField(upload_to='rumah_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.nama_pemilik)

class Fasos(models.Model):
    id_fasos = models.AutoField(primary_key=True)
    nama_perumahan = models.ForeignKey(Perumahan, on_delete=models.CASCADE)
    fasos = models.CharField(max_length=255)
    lokasi_fasos = models.GeometryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.fasos)

class RumahSusun(models.Model):
    id_rumah_susun = models.AutoField(primary_key=True)
    photo_rusun = models.ImageField(upload_to='rusun_photo/', blank=True, null=True)
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
    
class SebaranRumahLiar(models.Model):
    id_kelurahan = models.AutoField(primary_key=True)
    photo_ruli = models.ImageField(upload_to='ruli_photo/', blank=True, null=True)
    alamat_ruli = models.CharField(max_length=255)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    lokasi_ruli = models.GeometryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.alamat_ruli)
    
class Taman(models.Model):
    id_kelurahan = models.AutoField(primary_key=True)
    photo_taman = models.ImageField(upload_to='taman_photo/', blank=True, null=True)
    alamat_taman = models.CharField(max_length=255)
    nama_taman = models.CharField(max_length=255)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.nama_taman)
    
class AddRequest(models.Model):
    photo_rumah = models.ImageField(upload_to='rumah_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    photo_perumahan = models.ImageField(upload_to='perumahan_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    geometry = models.GeometryField(srid=4326)
    data = models.JSONField(blank=True, null=True)
    dibuat_oleh = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    disetujui = models.BooleanField(default=False)
    ditolak = models.BooleanField(default=False)

class UpdateRequest(models.Model):
    id_rumah = models.ForeignKey(Rumah, on_delete=models.CASCADE, blank=True, null=True)
    photo_rumah = models.ImageField(upload_to='rumah_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    photo_perumahan = models.ImageField(upload_to='perumahan_photo/', blank=True, null=True, storage=settings.SUPABASE_STORAGE_BACKEND)
    data = models.JSONField(blank=True, null=True)
    dibuat_oleh = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    disetujui = models.BooleanField(default=False)
    ditolak = models.BooleanField(default=False)