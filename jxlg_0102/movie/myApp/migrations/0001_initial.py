# Generated by Django 2.0 on 2019-06-24 06:04

import django.core.validators
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('length', models.CharField(max_length=50)),
                ('release_time', models.DateField()),
                ('score', models.FloatField()),
                ('score_num', models.IntegerField()),
                ('box_office', models.IntegerField()),
            ],
            options={
                'db_table': 'movie',
                'ordering': ['box_office'],
            },
        ),
        migrations.CreateModel(
            name='RtimeMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boxoffice_realtime', models.FloatField()),
                ('boxoffice_total', models.FloatField()),
                ('link', models.CharField(max_length=1000)),
                ('name', models.CharField(max_length=50)),
                ('releasetime', models.DateField()),
                ('score', models.FloatField()),
                ('star', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'realtime_movie',
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(6)])),
                ('telephone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('1[3456789]\\d{9}')])),
                ('email', models.EmailField(max_length=254)),
                ('password1', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(6)])),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
