import json
from base.models import Lokasi
from api.serializers import LokasiSerializer
from django.core.serializers import serialize
from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.geos import GEOSGeometry
from django.shortcuts import render
from rest_framework import generics, status


class MarkersMapView(TemplateView):
    template_name = "map.html"


class MarkersMapView(TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["markers"] = json.loads(serialize("geojson", Lokasi.objects.all()))
        return context
    
# class LokasiMarkerView(TemplateView):
#     template_name = "map.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["markers"] = json.loads(serialize("geojson", Lokasi.objects.all()))
#         return context

# class LokasiMarkerView(TemplateView):
#     template_name = "marker.html"
   
class LokasiMarkerView(APIView):
    def get(self, request, pk):
        point_markers = Lokasi.objects.all()

        # try:
        for point_marker in point_markers:
            point_str = f"SRID=4326;POINT ({point_marker.lon} {point_marker.lat})"
            point = GEOSGeometry(point_str)
            
            longitude = point.x
            latitude = point.y

                # Perform any additional operations with longitude and latitude here

                # Save longitude and latitude in the database
            point_marker.lon = longitude
            point_marker.lat = latitude
            point_marker.save()
        # except Exception as e:
        #     print(f"Error: {e}")
        return Response({
            "code": "200",
            "string_point": point_str
            # "longitude": point_marker.lon,
            # "latitude": point_marker.lat
        })
    
    
    # template_name = "marker.html"
    
    # def addLokasi(self, request):
    # queryset = Lokasi.objects.all()
    # serializer = LokasiSerializer
        
    #     data_point = serializer.data["point"]
    #     string_point = json.dumps(data_point)
    #     point = str(string_point[2:-1])
        
    #     return Response(data_point)
    #         {
    #             "coordinates": [serializer.data["point"].latitude, serializer.data["point"].longitude]
    #         })

# def create_marker_view(request):
#     return render(request, 'marker.html')

# class MarkerCreateView(generics.ListCreateAPIView):
#     queryset = Lokasi.objects.all()
#     serializer_class = LokasiSerializer
