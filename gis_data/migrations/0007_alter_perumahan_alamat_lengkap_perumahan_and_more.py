# Generated by Django 5.1.2 on 2025-04-16 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gis_data', '0006_alter_perumahan_kecamatan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perumahan',
            name='alamat_lengkap_perumahan',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AlterField(
            model_name='perumahan',
            name='kelurahan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gis_data.kelurahan'),
        ),
    ]
