# Generated by Django 2.2.7 on 2020-01-30 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20200130_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='Day',
            field=models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thur', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='MealType',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], max_length=50, unique=True),
        ),
    ]
