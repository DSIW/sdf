# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('language', models.CharField(max_length=100)),
                ('releaseDate', models.DateField(verbose_name='release_date')),
                ('pageNumber', models.IntegerField(default=1)),
                ('isbn10', models.CharField(max_length=100)),
                ('isbn13', models.CharField(max_length=100)),
                ('isOnStoreWindow', models.BooleanField(default=False)),
            ],
        ),
    ]
