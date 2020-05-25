# Generated by Django 3.0.4 on 2020-05-22 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0017_auto_20200521_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='template',
            field=models.CharField(choices=[('menus/details.html', 'Small'), ('menus/details2.html', 'Medium')], default='U', max_length=20),
        ),
        migrations.AlterField(
            model_name='price',
            name='size',
            field=models.CharField(choices=[('U', 'Only size'), ('XS', 'Extra small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra large'), ('Meal', 'Meal')], default='U', max_length=20),
        ),
    ]
