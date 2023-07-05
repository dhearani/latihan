import re
from django.contrib import admin
from django import forms
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis import admin as geoadmin

from .models import Lokasi

from django.contrib.gis import forms as gis_forms

class LocationAdminForm(gis_forms.ModelForm):
    class Meta:
        model = Lokasi
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        longitude = cleaned_data.get('lon')
        latitude = cleaned_data.get('lat')

        if longitude is not None and latitude is not None:
            point = Point(longitude, latitude)
            cleaned_data['point'] = point

        return cleaned_data



