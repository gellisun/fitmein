# Generated by Django 4.2.3 on 2023-08-07 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_profile_activities_today_alter_profile_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='activities_today',
        ),
        migrations.AlterField(
            model_name='profile',
            name='favorites',
            field=models.CharField(choices=[('RU', 'Running'), ('WL', 'Weight Lifting'), ('GC', 'Group Classes'), ('BR', 'Bike Riding'), ('TE', 'Tennis'), ('SQ', 'Squash'), ('WA', 'Walking'), ('BA', 'Badminton'), ('SW', 'Swimming'), ('WA', 'Walking'), ('HI', 'Hiking'), ('P', 'Pilates'), ('SU', 'Surfing'), ('SK', 'Skateboarding')], max_length=2),
        ),
    ]
