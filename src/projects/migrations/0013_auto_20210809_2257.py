# Generated by Django 3.2.3 on 2021-08-09 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_projectsection_instructor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningoutcome',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='titledescription',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
