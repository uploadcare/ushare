# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ushare.files.validators
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_obj', pyuploadcare.dj.models.FileField(null=True, verbose_name='file', validators=[ushare.files.validators.extension_validator, ushare.files.validators.size_validator])),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created', null=True)),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
            },
        ),
    ]
