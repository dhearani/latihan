# Generated by Django 4.1.6 on 2023-06-04 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_resep_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chef',
            name='nama',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='chef',
            name='spesialis',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='resep',
            name='chef',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='base.chef'),
        ),
    ]