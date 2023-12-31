# Generated by Django 4.2.3 on 2023-08-05 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
                ('icon', models.ImageField(max_length=255, upload_to=main_app.models.get_profile_image_filepath)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('age', models.IntegerField()),
                ('location', models.CharField()),
                ('is_couch_potato', models.BooleanField(default=True)),
                ('favorites', models.CharField(choices=[('RU', 'Running'), ('WL', 'Weight Lifting'), ('GC', 'Group Classes'), ('BR', 'Bike Riding'), ('TE', 'Tennis'), ('SQ', 'Squash'), ('WA', 'Walking'), ('BA', 'Badminton'), ('SW', 'Swimming'), ('WA', 'Walking'), ('HI', 'Hiking'), ('P', 'Pilates'), ('SU', 'Surfing'), ('SK', 'Skateboarding')], max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.AddField(
            model_name='badges',
            name='profile',
            field=models.ManyToManyField(to='main_app.profile'),
        ),
    ]
