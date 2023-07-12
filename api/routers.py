from rest_framework import routers
from .views import ChefViewSet, GaleriViewSet, GambarViewSet, RegisterViewSet, BerkasViewSet, UMKMViewSet, KoperasiViewSet, JenisProdukKoperasiViewSet, JenisProdukUMKMViewSet, PermintaanProdukViewSet

from django.urls import path

router = routers.SimpleRouter()
router.register(r'galeri', GaleriViewSet, basename='galeri')
router.register(r'gambar', GambarViewSet, basename='gambar')
router.register(r'account', RegisterViewSet, basename='account')
router.register(r'berkas', BerkasViewSet, basename='berkas')
# router.register(r'lokasi', LokasiViewSet, basename='lokasi')
router.register(r'koperasi', KoperasiViewSet, basename='koperasi')
router.register(r'umkm', UMKMViewSet, basename='umkm')
router.register(r'jp-koperasi', JenisProdukKoperasiViewSet, basename='jp-koperasi')
router.register(r'jp-umkm', JenisProdukUMKMViewSet, basename='jp-umkm')
router.register(r'permintaan-produk', PermintaanProdukViewSet, basename='permintaan-produk')

urlpatterns = [
    # path('', ForgotPasswordFormView.as_view()),
]

urlpatterns += router.urls