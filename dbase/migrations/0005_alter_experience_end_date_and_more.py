# Generated by Django 4.2.11 on 2024-06-12 21:20

import dbase.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbase', '0004_remove_profile_ba_end_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='end_date',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1960), dbase.models.max_value_current_year], verbose_name='End Year'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='start_date',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1960), dbase.models.max_value_current_year], verbose_name='Start Year'),
        ),
        migrations.CreateModel(
            name='Academic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('university', models.CharField(max_length=100)),
                ('phase', models.CharField(choices=[('Bachelor', 'Bachelor'), ('Master', 'Master'), ('Ph.D.', 'Ph.D.'), ('Postdoc', 'Postdoc'), ('Faculty', 'Faculty'), ('Other', 'Other')], max_length=50)),
                ('start_date', models.IntegerField(validators=[django.core.validators.MinValueValidator(1960), dbase.models.max_value_current_year], verbose_name='Start Year')),
                ('end_date', models.IntegerField(validators=[django.core.validators.MinValueValidator(1960), dbase.models.max_value_current_year], verbose_name='End Year')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academics', to='dbase.profile')),
            ],
        ),
    ]