# Generated by Django 4.2.11 on 2024-06-13 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbase', '0007_profile_place_profile_pronouns_profile_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='firstname',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='lastname',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
