# Generated by Django 3.2.3 on 2021-06-16 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='full_name',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
    ]
