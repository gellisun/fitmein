# Generated by Django 4.2.3 on 2023-08-08 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_merge_20230808_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='longitude',
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=250),
        ),
        migrations.AlterField(
            model_name='matcher',
            name='user',
            field=models.ManyToManyField(to='main_app.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='favorites',
            field=models.CharField(choices=[('RU', 'Running'), ('WL', 'Weight Lifting'), ('GC', 'Group Classes'), ('BR', 'Bike Riding'), ('TE', 'Tennis'), ('SQ', 'Squash'), ('WA', 'Walking'), ('BA', 'Badminton'), ('SW', 'Swimming'), ('WA', 'Walking'), ('HI', 'Hiking'), ('P', 'Pilates'), ('SU', 'Surfing'), ('SK', 'Skateboarding')], default='RU', max_length=2),
        ),
    ]
