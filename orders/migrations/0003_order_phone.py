# Generated by Django 3.0.4 on 2020-03-22 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200319_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
