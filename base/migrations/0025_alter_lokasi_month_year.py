# Generated by Django 4.2.2 on 2023-07-07 22:15

import base.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_lokasi_month_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lokasi',
            name='month_year',
            field=base.models.MonthYearField(null=True),
        ),
    ]