# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import phonenumber_field.modelfields
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_auto_20150131_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 5, 19, 51, 44, 280676, tzinfo=utc), verbose_name=b'appointment time and date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='patient',
            name='patient_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128),
            preserve_default=True,
        ),
    ]
