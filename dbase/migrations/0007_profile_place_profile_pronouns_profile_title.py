# Generated by Django 4.2.11 on 2024-06-13 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbase', '0006_rename_city_academic_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='place',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='pronouns',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
