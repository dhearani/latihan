from rest_framework import routers
from .views import ChefViewSet, GaleriViewSet, GambarViewSet, RegisterViewSet
from django.urls import path

router = routers.SimpleRouter()
router.register(r'galeri', GaleriViewSet, basename='galeri')
router.register(r'gambar', GambarViewSet, basename='gambar')
router.register(r'account', RegisterViewSet, basename='account')

urlpatterns = [
    # path('', ForgotPasswordFormView.as_view()),
]

urlpatterns += router.urls