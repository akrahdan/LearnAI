# Generated by Django 3.2.3 on 2021-08-18 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_auto_20210809_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='thumbnail_url',
            field=models.URLField(blank=True, max_length=120, null=True),
        ),
    ]
