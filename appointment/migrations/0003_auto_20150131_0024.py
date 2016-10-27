# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_auto_20150121_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(to='appointment.Patient', unique=True),
            preserve_default=True,
        ),
    ]
