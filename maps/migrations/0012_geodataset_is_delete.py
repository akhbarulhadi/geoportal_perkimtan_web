# Generated by Django 5.1.2 on 2025-07-13 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0011_remove_datamaps_id_field_maps_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='geodataset',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
