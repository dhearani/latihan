from django.contrib import admin
from django.contrib.gis import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis import admin as geoadmin
from base.models import Chef, Resep, Lokasi
from base.forms import LocationAdminForm
# Register your models here.

from django.contrib.admin.models import LogEntry

admin.site.register(Chef)
admin.site.register(Resep)
# admin.site.register(Lokasi)
# class MarkerAdmin(admin.GISModelAdmin):
#     list_display = ("nama", "lon", "lat")
    
# class PointMarkerAdmin(geoadmin.GeoModelAdmin):
#     form = PointMarkerAdminForm
@admin.register(Lokasi)
class LocationAdmin(OSMGeoAdmin):
    form = LocationAdminForm
    list_display = ('nama', 'lon', 'lat', 'point')