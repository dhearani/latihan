# Generated by Django 4.1.6 on 2023-06-07 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_chef_nama_alter_chef_spesialis_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kewarganegaraan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bangsa', models.CharField(max_length=50, null=True)),
                ('artis', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nat_artist', to='base.musisi')),
                ('chef', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nat_chef', to='base.chef')),
            ],
        ),
    ]
