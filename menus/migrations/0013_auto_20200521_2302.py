# Generated by Django 3.0.4 on 2020-05-22 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0012_auto_20200521_2300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['category__position']},
        ),
    ]