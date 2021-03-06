# Generated by Django 3.0.4 on 2020-06-14 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0040_auto_20200607_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='choice',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='menu',
            name='template',
            field=models.CharField(choices=[('menus/details.html', 'Small'), ('menus/details2.html', 'Medium'), ('menus/details2b.html', 'Medium B'), ('menus/details3.html', 'large'), ('menus/details4.html', 'X-large'), ('menus/details5.html', 'X-large 2'), ('menus/details6.html', 'Los_chachos'), ('menus/details7.html', 'Don_pedrito')], default='Unique', max_length=20),
        ),
    ]
