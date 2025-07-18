# Generated by Django 5.1.2 on 2025-04-16 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gis_data', '0010_rumah_photo_rumah'),
    ]

    operations = [
        migrations.AddField(
            model_name='rumah',
            name='alamat_rumah',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='rumah',
            name='jumlah_kk',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rumah',
            name='nama_pemilik',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='rumah',
            name='nilai_kesehatan',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rumah',
            name='nilai_keselamatan',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rumah',
            name='nilai_komponen',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rumah',
            name='status_luas',
            field=models.CharField(blank=True, choices=[('LUAS_RUMAH_CUKUP', 'Luas Rumah Cukup'), ('LUAS_RUMAH_KURANG', 'Luas Rumah Kurang')], max_length=30, null=True),
        ),
    ]
