# Generated by Django 4.2.2 on 2023-07-01 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_remove_lokasi_gmaps_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galeri',
            name='dok_url',
        ),
        migrations.RemoveField(
            model_name='gambar',
            name='foto_url',
        ),
    ]
