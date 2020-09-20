# Generated by Django 3.0.4 on 2020-09-20 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0049_auto_20200920_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='description',
        ),
        migrations.AddField(
            model_name='item',
            name='notes',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='notes'),
        ),
    ]
