# Generated by Django 5.1.2 on 2025-07-01 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gis_data', '0029_remove_updaterequest_nama_perumahan'),
    ]

    operations = [
        migrations.AddField(
            model_name='updaterequest',
            name='photo_perumahan',
            field=models.ImageField(blank=True, null=True, upload_to='perumahan_photo/'),
        ),
        migrations.AddField(
            model_name='updaterequest',
            name='photo_rumah',
            field=models.ImageField(blank=True, null=True, upload_to='rumah_photo/'),
        ),
    ]
