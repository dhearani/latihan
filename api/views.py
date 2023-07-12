import matplotlib.pyplot as plt
import numpy as np
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Album, Musisi, Chef, Resep, Lokasi, Kewarganegaraan, Galeri, Gambar, Berkas, UMKM, Koperasi, PermintaanProduk, JenisProdukKoperasi, JenisProdukUMKM
from .serializers import AlbumSerializer, MusisiSerializer, ChefSerializer, ResepSerializer, ChefsSerializer, BerkasSerializer, LokasiSerializer, GaleriSerializer, GambarSerializer, RegisterSerializer, MyTokenObtainPairSerializer
from .serializers import UMKMSerializer, KoperasiSerializer, JenisProdukKoperasiSerializer, JenisProdukUMKMSerializer, PermintaanProdukSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.gis.geos import GEOSGeometry
from io import BytesIO
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

class RegisterViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username']  # Replace with the fields you want to filter on
    search_fields = ['username']
    
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    
class LogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data['refresh_token']

            # Create a RefreshToken object from the refresh token
            token = RefreshToken(refresh_token)

            # Blacklist the refresh token to prevent its use
            token.blacklist()

            return Response({'message': 'Berhasil Logout'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'message':'Gagal Logout'}, status=status.HTTP_400_BAD_REQUEST)

  
class MusisiListView(generics.ListCreateAPIView):
    queryset = Musisi.objects.all()
    serializer_class = MusisiSerializer

class MusisiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MusisiSerializer
    queryset = Musisi.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.get_response()

    def perform_destroy(self, instance):
        instance.delete()

    def get_response(self):
        return Response({"message": "Musisi deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class AlbumListView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class ChefListView(generics.ListCreateAPIView):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer
    
class ChefViewSet(ModelViewSet):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer

    def list(self, request, pk=None):
        items = Chef.objects.all()
        serializer = ChefSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, validated_data):
        reseps_data = validated_data.pop('recipe')
        nats_data = validated_data.pop('nat_chef')
        koki = Chef.objects.create(**validated_data)
        for resep_data in reseps_data:
            Resep.objects.create(chef=koki, **resep_data)
        Kewarganegaraan.objects.create(chef=koki, **nats_data)
        return koki
    
class ChefView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChefSerializer
    queryset = Chef.objects.all()
    
    # def retrieve(self, request, pk, *args, **kwargs):
    #     items = Chef.objects.get(pk=pk)
    #     serializer = ChefsSerializer(items)
    #     return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
                "code": 200,
                "message": "data berhasil dihapus"
            },status=status.HTTP_204_NO_CONTENT)
    
    # def create(self, request, *args, **kwargs):
        
        
class ResepListView(generics.ListCreateAPIView):
    queryset = Resep.objects.all()
    serializer_class = ResepSerializer

class ResepView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResepSerializer
    queryset = Resep.objects.all()
    
class PieChartView(APIView):
    def get(self, request, format=None):
        # Perform the calculation and retrieve the graphic value
        chef_count = Chef.objects.count()
        musisi_count = Musisi.objects.count()
        
        # Prepare data for the pie chart
        labels = ['Chef', 'Musisi']
        sizes = np.array([chef_count, musisi_count])
        
        # Check if any counts are NaN
        if np.isnan(sizes).any():
            return HttpResponse("Data is not available for creating the pie chart.")
                
        plt.figure(figsize=(8, 8))
        plt.pie(sizes.flatten(), labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Pie Chart')  
        
        # Save the chart to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()

        # Return the chart as the response
        buffer.seek(0)
        return HttpResponse(buffer.getvalue(), content_type='image/png')
    
class LokasiView(generics.ListCreateAPIView):
        queryset = Lokasi.objects.all()
        serializer_class = LokasiSerializer
    # def get(self, request):
        # point_markers = Lokasi.objects.all()

        # for point_marker in point_markers:
        #     longitude = point_marker.point.x
        #     latitude = point_marker.point.y

        #     # Perform any additional operations with longitude and latitude here

        #     # Save longitude and latitude in the database
        #     point_marker.lon = longitude
        #     point_marker.lat = latitude
        #     point_marker.save()
        
            # return Response(serializer.data
            # # {
            # # "code": "200",
            # # "longitude": point_marker.lon,
            # # "latitude": point_marker.lat
            # # }
            # )

class GaleriViewSet(ModelViewSet):
    queryset = Galeri.objects.all()
    serializer_class = GaleriSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tahun']  # Replace with the fields you want to filter on
    search_fields = ['tahun']
    
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return self.get_response()

    # def perform_destroy(self, instance):
    #     instance.delete()

    # def get_response(self):
    #     return Response({"message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
class GambarViewSet(ModelViewSet):
    queryset = Gambar.objects.all()
    serializer_class = GambarSerializer
    
class BerkasViewSet(ModelViewSet):
    queryset = Berkas.objects.all()
    serializer_class = BerkasSerializer

class KoperasiViewSet(ModelViewSet):
    queryset = Koperasi.objects.all()
    serializer_class = KoperasiSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nama']  # Replace with the fields you want to filter on
    search_fields = ['nama']

class UMKMViewSet(ModelViewSet):
    queryset = UMKM.objects.all()
    serializer_class = UMKMSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nama_usaha']  # Replace with the fields you want to filter on
    search_fields = ['nama_usaha']

class JenisProdukUMKMViewSet(ModelViewSet):
    queryset = JenisProdukUMKM.objects.all()
    serializer_class = JenisProdukUMKMSerializer
    
class JenisProdukKoperasiViewSet(ModelViewSet):
    queryset = JenisProdukKoperasi.objects.all()
    serializer_class = JenisProdukKoperasiSerializer
    
class PermintaanProdukViewSet(ModelViewSet):
    queryset = PermintaanProduk.objects.all()
    serializer_class = PermintaanProdukSerializer


from django.db.models import Avg, StdDev, Count, Sum, Window
from collections import Counter
class Contoh(APIView):
    def get(self, request):
        # x_pos = [0, 1, 2, 3]
        # x_axis = ['A', 'B', 'C', 'D']

        # plt.plot(x_pos, [5, 2, 7, 9])

        # plt.xticks(x_pos, x_axis)

        # plt.show()
        
        x_pos = [0, 1, 2, 3]
        x_axis = ['A', 'B', 'C', 'D']
        y_values = [5, 2, 7, 9]

        plt.bar(x_pos, y_values)
        plt.xticks(x_pos, x_axis)

        plt.show()

import math
import numpy as np
# Bullwhip Effect KUMKM
class BullwhipEffectUMKM(APIView):
    def get(self, request, format=None):
        queryset = PermintaanProduk.objects.all()
        
        permintaan = list(queryset.values_list('permintaan', flat=True))
        produksi = list(queryset.values_list('produksi', flat=True))
        bulan = queryset.values_list('bulan', flat=True)
        count_bulan = len(bulan)
        
        print("jumlah bulan", count_bulan)
        
        avg_pm = np.mean(permintaan)
        avg_pd = np.mean(produksi)

        std_pm = np.std(permintaan, ddof=1)
        std_pd = np.std(produksi, ddof=1)

        koef_pm = std_pm/avg_pm
        koef_pd = std_pd/avg_pd
        
        be = koef_pd / koef_pm
        
        par = (1+(2*1/count_bulan)+(1**2/(count_bulan**2)))
        print(par)
        
        if(be > par):
            print(False)
        else:
            print(True)
            
        return Response(permintaan)

# Permintaan Produk UMKM
class MovingAverageUMKM(APIView):
    def get(self):
        distinct_komoditi = UMKM.objects.values_list('JenisProdukUMKM__komoditi', flat=True).distinct()
        monthly_permintaan = PermintaanProduk.objects.values('bulan').annotate(total_permintaan=Sum('permintaan'))
        sum_permintaan = PermintaanProduk.objects.aggregate(Sum('permintaan'))
        ma = Sum(Count(monthly_permintaan)) / Count(distinct_komoditi)
        
        return ma
    
# Rata" Kinerja Pemasok UMKM
class AverageSupplierPerfUMKM(APIView):
    def get(self):
        # tabel prioritas
    
        return