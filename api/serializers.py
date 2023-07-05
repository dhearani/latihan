from rest_framework import serializers
from base.models import Album, Musisi, Chef, Resep, Kewarganegaraan, Lokasi, Gambar, Galeri, Berkas, Detail
from drf_writable_nested import WritableNestedModelSerializer, NestedUpdateMixin
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from cloudinary import uploader
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib import messages
import cloudinary
import cloudinary.uploader

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    detail = DetailSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'detail')
        
    def create(self, validated_data, *args, **kwargs):
        detail_data = validated_data.pop('detail')
        nik = detail_data['nik']

        instance = super().create(validated_data)
        instance.set_password(nik)
        
        Detail.objects.create(user=instance, **detail_data)
            
        instance.save()
        return instance
    
    def retrieve(self, instance):
        return instance
    
    def update(self, instance, validated_data):
        detail_data = validated_data.pop('detail', [])
        detail = instance.detail
        
        instance = super().update(instance, validated_data)
        
        detail.nik = detail_data.pop('nik')
        detail.telepon = detail_data.pop('telepon')
        foto_profil = detail_data.pop('foto_profil', detail.foto_profil)
        if foto_profil:
            cloudinary_storage = RawMediaCloudinaryStorage()
            detail.foto_profil = cloudinary_storage.save(foto_profil.name, foto_profil)
        detail.save()
        
        instance.save()
        return instance
 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token       

class KewarganegaraanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kewarganegaraan
        fields = ('id', 'chef', 'artis', 'bangsa')

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'artis', 'album_nama', 'num_star')
        
class MusisiSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    album_musisi = AlbumSerializer()
    nat_artis = KewarganegaraanSerializer()
    
    class Meta:
        model = Musisi
        fields = ('id', 'nama', 'instrumen', 'album_musisi', 'nat_artis')
        
    def create(self, validated_data):
        albums_data = validated_data.pop('album_musisi')
        nats_data = validated_data.pop('nat_artis')
        musisi = Musisi.objects.create(**validated_data)
        # for album_data in albums_data:
        Album.objects.create(artis=musisi, **albums_data)
        Kewarganegaraan.objects.create(artis=musisi, **nats_data)
        return musisi
    
    def update(self, instance, validated_data):
        # Update the instance with the validated data
        instance.nama = validated_data.get('nama', instance.nama)
        instance.instrumen = validated_data.get('instrumen', instance.instrumen)
        
        album_musisi = validated_data.get('album_musisi')
        instance.album_musisi.album_nama = album_musisi.get('album_nama')
        instance.album_musisi.num_star = album_musisi.get('num_star')
        
        nat_artis = validated_data.get('nat_artis')
        instance.nat_artis.bangsa = nat_artis.get('bangsa')
        # Update other fields as needed

        # Save the updated instance
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     albums_data = validated_data.pop('album_musisi')
    #     albums = instance.album_musisi
    #     albums = list(albums)
    #     instance.nama = validated_data.get('nama', instance.nama)
    #     instance.instrumen = validated_data.get('instrumen', instance.instrumen)
    #     instance.save()

    #     for album_data in albums_data:
    #         album = albums.pop(0)
    #         album.album_nama = album_data.get('album_nama', album.album_nama)
    #         album.num_star = album_data.get('num_star', album.num_star)
    #         album.save()
    #     return instance
        
class ResepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resep
        fields = ('id', 'chef', 'nama_resep', 'rating')
        
class ChefSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    recipe = ResepSerializer(many=True)
    nat_chef = KewarganegaraanSerializer()
    
    class Meta:
        model = Chef
        fields = ('id', 'nama', 'spesialis', 'recipe', 'nat_chef')
        
    def create(self, validated_data):
        reseps_data = validated_data.pop('recipe')
        nats_data = validated_data.pop('nat_chef')
        koki = Chef.objects.create(**validated_data)
        for resep_data in reseps_data:
            Resep.objects.create(chef=koki, **resep_data)
        Kewarganegaraan.objects.create(chef=koki, **nats_data)
        return koki
    
    def update(self, instance, validated_data):
        reseps_data = validated_data.pop('recipe')
        reseps = (instance.recipe).all()
        reseps = list(reseps)
        instance.nama = validated_data.get('nama', instance.nama)
        instance.spesialis = validated_data.get('spesialis', instance.spesialis)
        instance.save()

        for resep_data in reseps_data:
            resep = reseps.pop(0)
            resep.nama_resep = resep_data.get('nama_resep', resep.nama_resep)
            resep.rating = resep_data.get('rating', resep.rating)
            resep.save()
        
        nat_chef = validated_data.get('nat_chef')
        instance.nat_chef.bangsa = nat_chef.get('bangsa')
        
        return instance
    
        
class ChefsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = '__all__'
        
class LokasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lokasi
        fields = '__all__'

class BerkasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Berkas
        fields = ('id', 'galeri', 'pdf', 'ket')
        
    def create(self, validated_data):
        pdf = validated_data.pop('pdf', None)
        
        child_instance = super().create(validated_data)
        if pdf:
            cloudinary_storage = RawMediaCloudinaryStorage()
            child_instance.foto = cloudinary_storage.save(pdf.name, pdf)
        
        child_instance.save()
        return child_instance
        
class GambarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Gambar
        fields = ('id', 'galeri', 'foto', 'ket')
        
    def create(self, validated_data):
        foto = validated_data.pop('foto', None)
        
        child_instance = super().create(validated_data)
        if foto:
            cloudinary_storage = RawMediaCloudinaryStorage()
            child_instance.foto = cloudinary_storage.save(foto.name, foto)
        
        child_instance.save()
        return child_instance
    
    def update(self, instance, validated_data):
        foto = validated_data.pop('foto', None)
        foto_url = validated_data.pop('foto_url', None)
        instance = super().update(instance, validated_data)
        if foto:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.foto = cloudinary_storage.save(foto.name, foto)
        
        if foto_url:
            instance.foto_url = foto_url
        
        instance.save()
        return instance
        
class GaleriSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    gambar = GambarSerializer(many=True)
    berkas = BerkasSerializer()
    
    class Meta:
        model = Galeri
        fields = ['id', 'nama', 'dokumen', 'tahun', 'gambar', 'berkas']
    
    def create(self, validated_data, *args, **kwargs):
        gambars_data = validated_data.pop('gambar', [])
        berkas_data = validated_data.pop('berkas')
        # nama = validated_data.pop('nama', None)
        dokumen = validated_data.pop('dokumen', None)
        # tahun = validated_data.pop('tahun', None)
        instance = super().create(validated_data)
        if dokumen:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dokumen = cloudinary_storage.save(dokumen.name, dokumen)
            
        # if nama:
        #     instance.nama = nama
            
        # if tahun:
        #     instance.tahun = tahun
            
        for gambar_data in gambars_data:
            gambar_data['galeri'] = instance.pk  # Set the parent instance for the child
            gambar_serializer = GambarSerializer(data=gambar_data)
            gambar_serializer.is_valid(raise_exception=True)
            gambar_serializer.save()
        
        Berkas.objects.create(galeri=instance, **berkas_data)
            
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        old_dokumen = instance.dokumen
        print(old_dokumen)
        # Delete the old file from Cloudinary
        if old_dokumen:
            cloudinary_storage = RawMediaCloudinaryStorage
            hasil = cloudinary_storage.destroy(old_dokumen.name)
            print("hasil old_dokumen", hasil)
            
        gambars_data = validated_data.pop('gambar', [])
        gambars = (instance.gambar).all()
        gambars = list(gambars)
        
        for images in gambars:
            old_gambar = images.foto
            print(old_gambar)
            if old_gambar:
                cloudinary_storage = RawMediaCloudinaryStorage
                hasil1 = cloudinary_storage.destroy(old_gambar.name)
                print("hasil old_gambar", hasil1)
        
        berkass_data = validated_data.pop('berkas', [])
        berkass = instance.berkas
            
        old_berkas = berkass.pdf
        print(old_berkas)
        if old_berkas:
            cloudinary_storage = RawMediaCloudinaryStorage
            hasil2 = cloudinary_storage.destroy(old_berkas.name)
            print("hasil old_berkas", hasil2)
        
        # instance.nama = validated_data.pop('nama', instance.nama)
        dokumen = validated_data.pop('dokumen', instance.dokumen)
        # instance.tahun = validated_data.pop('tahun', instance.tahun)
        
        instance = super().update(instance, validated_data)
        
        if dokumen:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dokumen = cloudinary_storage.save(dokumen.name, dokumen)
        
        for gambar_data in gambars_data:
            gambar = gambars.pop(0)
            image = gambar_data.pop('foto', gambar.foto)
            gambar.ket = gambar_data.pop('ket', gambar.ket)
            if image:
                cloudinary_storage = RawMediaCloudinaryStorage()
                gambar.foto = cloudinary_storage.save(image.name, image)
            gambar.save()
        
        berkass.ket = berkass_data.pop('ket')
        file = berkass_data.pop('pdf', berkass.pdf)
        if file:
            cloudinary_storage = RawMediaCloudinaryStorage()
            berkass.pdf = cloudinary_storage.save(file.name, file)
        berkass.save()
            
        instance.save()
        return instance
    
    def retrieve(self, instance):
        return instance
    
    def destroy(self, instance, request, *args, **kwargs):
        instance.delete()
        # return Response({"Success": "Data deleted successfully"}, status=status.HTTP_202_OK)
        return messages.success(self.request, 'Form submission successful')