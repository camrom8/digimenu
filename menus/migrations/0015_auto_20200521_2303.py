# Generated by Django 3.0.4 on 2020-05-22 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0014_auto_20200521_2303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['category__position']},
        ),
    ]
