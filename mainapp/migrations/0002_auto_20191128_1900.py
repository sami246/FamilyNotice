# Generated by Django 2.2.7 on 2019-11-28 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Group',
            new_name='Family',
        ),
        migrations.RenameField(
            model_name='family',
            old_name='nameofGroup',
            new_name='nameofFamily',
        ),
        migrations.AlterField(
            model_name='list',
            name='task',
            field=models.ManyToManyField(to='mainapp.Task'),
        ),
    ]