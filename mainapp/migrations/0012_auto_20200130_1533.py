# Generated by Django 2.2.7 on 2020-01-30 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20200130_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='type',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type', to='mainapp.MealType'),
        ),
    ]
