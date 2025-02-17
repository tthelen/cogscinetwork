# Generated by Django 4.2.11 on 2024-07-17 21:28

import dbase.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbase', '0012_profile_homepage_profile_instagram_profile_linkedin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academic',
            name='end_date',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1960), dbase.models.max_value_current_year], verbose_name='End Year'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='end_date',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1960), dbase.models.max_value_current_year], verbose_name='End Year'),
        ),
    ]
