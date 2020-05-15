# Generated by Django 3.0.6 on 2020-05-11 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0004_auto_20200510_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='price_str',
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='price_num')),
                ('price_str', models.CharField(max_length=10, verbose_name='price')),
                ('size', models.PositiveSmallIntegerField(max_length=10, verbose_name='size')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='menus.Item')),
            ],
        ),
    ]
