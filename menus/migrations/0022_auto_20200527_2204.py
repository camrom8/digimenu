# Generated by Django 3.0.4 on 2020-05-28 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0021_auto_20200527_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='title_slug',
            field=models.SlugField(unique=True),
        ),
    ]