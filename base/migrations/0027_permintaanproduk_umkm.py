# Generated by Django 4.2.2 on 2023-07-10 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_koperasi_permintaanproduk_umkm_jenisprodukumkm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='permintaanproduk',
            name='umkm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permintaan_produk_umkm', to='base.umkm'),
        ),
    ]