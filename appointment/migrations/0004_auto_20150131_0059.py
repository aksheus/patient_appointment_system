# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_auto_20150131_0024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='patient',
        ),
        migrations.AddField(
            model_name='patient',
            name='appointment',
            field=models.ForeignKey(null=True, blank=True, to='appointment.Appointment', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 30, 19, 29, 11, 957202, tzinfo=utc), verbose_name=b'appointment time and date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_problem',
            field=models.TextField(default=b'no appointment remove this', max_length=100),
            preserve_default=True,
        ),
    ]
