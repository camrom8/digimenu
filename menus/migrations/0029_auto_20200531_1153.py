# Generated by Django 3.0.4 on 2020-05-31 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0028_auto_20200531_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productincart',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=6),
        ),
    ]
