# Generated by Django 4.2.3 on 2023-08-07 15:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0007_matcher_created_at_matcher_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matcher',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
