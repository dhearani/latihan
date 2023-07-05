from django.urls import path

from map.views import MarkersMapView, LokasiMarkerView

app_name = "markers"

urlpatterns = [
    path("map/", MarkersMapView.as_view()),
    path('marker/<int:pk>/', LokasiMarkerView.as_view()),
    # path('create/', MarkerCreateView.as_view(), name='create_marker'),
    # path('create-marker-view/', create_marker_view, name='create_marker_view'),
]