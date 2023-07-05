from django.urls import path
from . import views
from api.views import MusisiListView, MusisiView, AlbumListView, ChefListView, ChefView, ResepListView, ResepView, PieChartView, LokasiView, MyObtainTokenPairView, LogoutView

urlpatterns = [
     path('MusisiListView/', MusisiListView.as_view()),
     path('MusisiView/<int:pk>/', MusisiView.as_view()),
     path('AlbumListView/', AlbumListView.as_view()),
     path('chef/', ChefListView.as_view()),
     path('chef/<int:pk>/', ChefView.as_view()),
     path('ResepListView/', ResepListView.as_view()),
     path('ResepView/', ResepView.as_view()),
     path('pie-chart/', PieChartView.as_view()),
     path('lokasi/', LokasiView.as_view()),
     path('login/', MyObtainTokenPairView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
     # path('marker/', LokasiMarkerView.as_view()),
     # path('galeri/<int:pk>/', GaleriViewSet.as_view({'get': 'list', 'get': 'retrieve', 'post': 'create', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]
