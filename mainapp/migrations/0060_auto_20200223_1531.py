# Generated by Django 2.2.7 on 2020-02-23 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0059_family_calid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='calId',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
