# Generated by Django 3.0.8 on 2020-09-06 02:42

import datetime
from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_tsdocument_trigger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='GPS Coord'),
        ),
        migrations.AddField(
            model_name='opening',
            name='entry_hash',
            field=models.CharField(default=datetime.datetime.now, max_length=200, unique=True, verbose_name='Title Hash'),
            preserve_default=False,
        ),
    ]