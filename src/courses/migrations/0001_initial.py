# Generated by Django 3.2.3 on 2021-06-15 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=220)),
                ('description', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, default=1, null=True)),
                ('level', models.CharField(choices=[('basic', 'Basic'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('deep', 'Deep Dive'), ('featured', 'Featured')], default='basic', max_length=120)),
                ('video_url', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('state', models.CharField(choices=[('LIVE', 'Live'), ('DR', 'Draft'), ('PD', 'Pending'), ('DEL', 'Deleted')], default='DR', max_length=4)),
                ('publish_timestamp', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=39.99, max_digits=20, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='categories.category')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRelated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_item', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
            options={
                'ordering': ['order', '-timestamp'],
            },
        ),
    ]
