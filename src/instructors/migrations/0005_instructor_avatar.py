# Generated by Django 3.2.3 on 2021-08-03 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0004_instructor_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='avatar',
            field=models.URLField(blank=True, max_length=220, null=True),
        ),
    ]
