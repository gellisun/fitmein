# Generated by Django 4.2.3 on 2023-08-07 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_profile_short_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='short_bio',
        ),
    ]
