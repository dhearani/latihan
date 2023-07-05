from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group, User

# from geoposition.fields import GeopositionField

# Create your models here.
class Detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nik = models.CharField(max_length=16, unique=True)
    telepon = models.CharField(max_length=13)
    foto_profil = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)

class Musisi(models.Model):
    nama = models.CharField(max_length=100, null=True)
    instrumen = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.nama
    
class Album(models.Model):
    artis = models.OneToOneField(Musisi, on_delete=models.CASCADE, null=True, related_name='album_musisi')
    album_nama = models.CharField(max_length=200)
    num_star = models.IntegerField(null=True)
    
    def __str__(self):
        return self.album_nama
    
class Chef(models.Model):
    nama = models.CharField(max_length=50, null=True)
    spesialis = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.nama
    
class Resep(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, null=True, related_name='recipe')
    nama_resep = models.CharField(max_length=50)
    rating = models.IntegerField(null=True)
    
    def __str__(self):
        return self.nama_resep
    
class Kewarganegaraan(models.Model):
    chef = models.OneToOneField(Chef, on_delete=models.CASCADE, null=True, related_name='nat_chef')
    artis = models.OneToOneField(Musisi, on_delete=models.CASCADE, null=True, related_name='nat_artis')
    bangsa = models.CharField(max_length=50, null=True)

class Lokasi(models.Model):
    nama = models.CharField(max_length=50)
    lat = models.FloatField(null=True, blank=True)   
    lon = models.FloatField(null=True, blank=True)
    point = models.PointField(null=True)
    
    def __str__(self):
        return self.nama
    
class Galeri(models.Model):
    nama = models.CharField(max_length=10)
    dokumen = models.FileField((""), upload_to='assets', null=True)
    tahun = models.IntegerField(null=True)
    
class Gambar(models.Model):
    galeri = models.ForeignKey(Galeri, on_delete=models.CASCADE, null=True, related_name='gambar')
    foto = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None) 
    ket = models.CharField(max_length=10, null=True)  
    
class Berkas(models.Model):
    galeri = models.OneToOneField(Galeri, on_delete=models.CASCADE, null=True, related_name='berkas')
    pdf = models.FileField((""), upload_to='assets', null=True)
    ket = models.CharField(max_length=10, null=True)
    