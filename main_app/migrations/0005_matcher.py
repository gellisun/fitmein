# Generated by Django 4.2.3 on 2023-08-06 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_profile_location_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosen_activities', models.CharField(choices=[('RU', 'Running'), ('WL', 'Weight Lifting'), ('GC', 'Group Classes'), ('BR', 'Bike Riding'), ('TE', 'Tennis'), ('SQ', 'Squash'), ('WA', 'Walking'), ('BA', 'Badminton'), ('SW', 'Swimming'), ('WA', 'Walking'), ('HI', 'Hiking'), ('P', 'Pilates'), ('SU', 'Surfing'), ('SK', 'Skateboarding')], max_length=2)),
                ('user', models.ManyToManyField(to='main_app.profile')),
            ],
        ),
    ]
