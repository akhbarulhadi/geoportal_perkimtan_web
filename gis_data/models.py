from django.contrib.gis.db import models

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
    lokasi_perumahan = models.GeometryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.nama_perumahan)

class Rumah(models.Model):
    JENIS_CHOICES = [
        ('RUMAH_LAYAK_HUNI', 'Rumah Layak Huni'),
        ('RUMAH_TIDAK_LAYAK_HUNI', 'Rumah Tidak Layak Huni'),
    ]
    id_rumah = models.AutoField(primary_key=True)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    nama_perumahan = models.ForeignKey(Perumahan, on_delete=models.CASCADE)
    block = models.CharField(max_length=255)
    status_rumah = models.CharField(max_length=30, choices=JENIS_CHOICES)
    rawan_bencana = models.BooleanField(default=False)
    # photo_rumah = models.ImageField(upload_to='datasets_photos/',blank=True, null=True )
    lokasi_rumah = models.GeometryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.id_rumah)


# class PerumahanPermukiman(models.Model):
#     name = models.CharField(max_length=255)
#     location = models.GeometryField(blank=True, null=True)
#     category = models.CharField(max_length=100, blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     last_modified = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "{}".format(self.name)
