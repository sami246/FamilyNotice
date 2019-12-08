# Generated by Django 2.2.7 on 2019-11-28 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOfBirth', models.DateField()),
                ('userType', models.CharField(choices=[('FamilyMember', 'Regular Family Member'), ('Gaurdian', 'Gaurdian')], max_length=50)),
                ('profilePic', models.ImageField(default='static/empty-photo.jpg', upload_to='static/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('description', models.TextField()),
                ('assignTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assign_to', to='mainapp.Member')),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ManyToManyField(to='mainapp.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameofGroup', models.CharField(max_length=30)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.List')),
                ('members', models.ManyToManyField(to='mainapp.Member')),
            ],
        ),
        migrations.CreateModel(
            name='EventEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=30)),
                ('membersInvolved', models.ManyToManyField(to='mainapp.Member')),
            ],
        ),
    ]
