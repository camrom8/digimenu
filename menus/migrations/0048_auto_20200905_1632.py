# Generated by Django 3.0.4 on 2020-09-05 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0047_auto_20200905_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ingredients',
            field=models.CharField(blank=True, max_length=255, verbose_name='ingredients'),
        ),
    ]
