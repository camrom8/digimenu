# Generated by Django 3.0.4 on 2020-05-28 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0019_auto_20200527_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='title_slug',
            field=models.SlugField(default='hello'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=20, verbose_name='title'),
        ),
    ]
