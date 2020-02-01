# Generated by Django 2.2.7 on 2020-01-30 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_auto_20200130_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='mealType',
            field=models.CharField(choices=[('MonB', 'Monday Breakfast'), ('TueB', 'Tuesday Breakfast'), ('WedB', 'Wednesday Breakfast'), ('ThurB', 'Thursday Breakfast'), ('FriB', 'Friday Breakfast'), ('SatB', 'Saturday Breakfast'), ('SunB', 'Sunday Breakfast'), ('MonL', 'Monday Lunch'), ('TueL', 'Tuesday Lunch'), ('WedL', 'Wednesday Lunch'), ('ThurL', 'Thursday Lunch'), ('FriL', 'Friday Lunch'), ('SatL', 'Saturday Lunch'), ('SunL', 'Sunday Lunch'), ('MonD', 'Monday Dinner'), ('TueD', 'Tuesday Dinner'), ('WedD', 'Wednesday Dinner'), ('ThurD', 'Thursday Dinner'), ('FriD', 'Friday Dinner'), ('SatD', 'Saturday Dinner'), ('SunD', 'Sunday Dinner')], max_length=50, unique=True),
        ),
    ]
