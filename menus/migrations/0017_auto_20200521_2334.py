# Generated by Django 3.0.4 on 2020-05-22 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0016_auto_20200521_2307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['position']},
        ),
    ]
