# Generated by Django 3.0.4 on 2020-05-30 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0021_auto_20200528_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='menus.Order')),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inCart', to='menus.Price')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(related_name='orders', through='menus.ProductInCart', to='menus.Price'),
        ),
        migrations.CreateModel(
            name='AddsOn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='price_num')),
                ('price_str', models.CharField(max_length=10, verbose_name='price')),
                ('product', models.ManyToManyField(related_name='adds_ons', to='menus.ProductInCart')),
            ],
        ),
    ]