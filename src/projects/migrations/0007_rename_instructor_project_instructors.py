# Generated by Django 3.2.3 on 2021-08-05 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20210805_2056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='instructor',
            new_name='instructors',
        ),
    ]
