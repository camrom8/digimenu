# Generated by Django 3.0.6 on 2020-05-09 00:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.BigIntegerField(blank=True)),
                ('nickname', models.CharField(default='none', max_length=20, verbose_name='nickname')),
                ('gender', models.CharField(choices=[('MA', 'Male'), ('FE', 'Femele'), ('OT', 'other')], default='OT', max_length=2, verbose_name='gender')),
                ('city', models.CharField(blank=True, max_length=30, verbose_name='city')),
                ('photo', models.ImageField(default='/profiles/profile.jpg', upload_to='media/profiles')),
                ('company', models.CharField(blank=True, max_length=30, verbose_name='company')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
