# Generated by Django 3.0.4 on 2020-05-31 00:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menus', '0024_addson_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productincart',
            name='total',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=6, verbose_name='price_num'),
            preserve_default=False,
        ),
    ]
