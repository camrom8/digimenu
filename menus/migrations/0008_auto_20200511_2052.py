# Generated by Django 3.0.6 on 2020-05-12 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0007_auto_20200511_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='size',
            field=models.CharField(choices=[('Only size', 'Only size'), ('Small', 'Small'), ('Extra small', 'Extra small'), ('medium', 'medium'), ('Large', 'Large'), ('Extra Large', 'Extra large'), ('combo', 'Combo')], default='Only size', max_length=20),
        ),
    ]
