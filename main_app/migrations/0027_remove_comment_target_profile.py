# Generated by Django 4.2.3 on 2023-08-10 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0026_comment_target_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='target_profile',
        ),
    ]
