# Generated by Django 2.2.7 on 2020-03-16 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20200316_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='chatroom',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Chatroom'),
        ),
        migrations.AlterField(
            model_name='family',
            name='choreList',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.ChoreList'),
        ),
        migrations.AlterField(
            model_name='family',
            name='mealPlan',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.MealWeek'),
        ),
    ]