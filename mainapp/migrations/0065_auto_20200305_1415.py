# Generated by Django 2.2.7 on 2020-03-05 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0064_auto_20200223_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rewards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('points', models.PositiveIntegerField(default='0')),
            ],
        ),
        migrations.RemoveField(
            model_name='chores',
            name='assignChoreTo',
        ),
        migrations.AddField(
            model_name='chores',
            name='assignChoreTo',
            field=models.ManyToManyField(blank=True, to='mainapp.Member'),
        ),
        migrations.AlterField(
            model_name='chores',
            name='reward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='author', to='mainapp.Rewards'),
        ),
        migrations.CreateModel(
            name='ChoreList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chores', models.ManyToManyField(blank=True, to='mainapp.Chores')),
                ('rewards', models.ManyToManyField(blank=True, to='mainapp.Rewards')),
            ],
        ),
        migrations.AddField(
            model_name='family',
            name='choreList',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.ChoreList'),
        ),
    ]
