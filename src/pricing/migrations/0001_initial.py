# Generated by Django 3.2.3 on 2021-08-01 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0007_course_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(choices=[('50', '50'), ('100', '100'), ('200', '200'), ('300', '300'), ('400', '400'), ('500', '500')], default='50', max_length=5)),
                ('currency', models.CharField(choices=[('GHS', 'GHS'), ('USD', 'USD'), ('GBP', 'GBP')], default='USD', max_length=4)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pricing', to='courses.course')),
            ],
        ),
    ]
