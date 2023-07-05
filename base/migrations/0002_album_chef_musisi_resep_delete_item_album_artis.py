# Generated by Django 4.1.6 on 2023-05-31 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_nama', models.CharField(max_length=200)),
                ('num_star', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50)),
                ('spesialis', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Musisi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100, null=True)),
                ('instrumen', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_resep', models.CharField(max_length=50)),
                ('chef', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resep_chef', to='base.chef')),
            ],
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.AddField(
            model_name='album',
            name='artis',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='album_musisi', to='base.musisi'),
        ),
    ]
