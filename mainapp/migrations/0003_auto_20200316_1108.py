# Generated by Django 2.2.7 on 2020-03-16 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20200315_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimReward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='mainapp.Member')),
            ],
        ),
        migrations.AddField(
            model_name='chorelist',
            name='claim',
            field=models.ManyToManyField(blank=True, to='mainapp.ClaimReward'),
        ),
    ]
