# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0002_user_emailconfirm'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmEmail',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('uuid', models.CharField(max_length=50)),
                ('user', models.OneToOneField(to='appuser.User')),
            ],
        ),
    ]
