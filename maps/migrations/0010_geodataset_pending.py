# Generated by Django 5.1.2 on 2025-07-03 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0009_remove_geodataset_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='geodataset',
            name='pending',
            field=models.BooleanField(default=True),
        ),
    ]
