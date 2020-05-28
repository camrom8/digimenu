# Generated by Django 3.0.4 on 2020-05-28 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0020_auto_20200527_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=20, unique=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title_slug',
            field=models.CharField(max_length=25, unique=True, verbose_name='title'),
        ),
    ]