# Generated by Django 3.0.4 on 2020-05-22 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0010_auto_20200521_2245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-category']},
        ),
    ]
