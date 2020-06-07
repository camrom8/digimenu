# Generated by Django 3.0.4 on 2020-06-07 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0039_auto_20200606_1858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['menu', 'position']},
        ),
        migrations.AlterField(
            model_name='menu',
            name='template',
            field=models.CharField(choices=[('menus/details.html', 'Small'), ('menus/details2.html', 'Medium'), ('menus/details3.html', 'large'), ('menus/details4.html', 'X-large'), ('menus/details5.html', 'X-large 2'), ('menus/details6.html', 'X-large 3')], default='Unique', max_length=20),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=40, unique=True, verbose_name='title'),
        ),
    ]
