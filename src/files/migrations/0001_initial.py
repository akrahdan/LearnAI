# Generated by Django 3.2.3 on 2021-06-15 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='S3File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=220, null=True)),
                ('key', models.TextField()),
                ('filetype', models.CharField(default='video/mp4', max_length=120)),
                ('uploaded', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('size', models.DecimalField(blank=True, decimal_places=4, max_digits=30, null=True)),
                ('duration', models.DecimalField(blank=True, decimal_places=6, max_digits=30, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=220, null=True)),
                ('key', models.TextField()),
                ('filetype', models.CharField(default='video/mp4', max_length=120)),
                ('uploaded', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('size', models.DecimalField(blank=True, decimal_places=4, max_digits=30, null=True)),
                ('duration', models.DecimalField(blank=True, decimal_places=6, max_digits=30, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='courses.course')),
            ],
        ),
    ]
