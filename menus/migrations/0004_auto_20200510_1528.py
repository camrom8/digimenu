# Generated by Django 3.0.6 on 2020-05-10 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_auto_20200510_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=models.TextField(max_length=500, verbose_name='description'),
        ),
    ]
