# Generated by Django 3.0.4 on 2020-03-24 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20200323_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='color',
            field=models.CharField(default='color', max_length=20),
            preserve_default=False,
        ),
    ]
