# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import appointment.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appointment_datetime', models.DateTimeField(verbose_name=b'appointment time and date')),
                ('fresh_or_review', models.BooleanField(default=False)),
                ('appointment_problem', models.TextField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_name', models.CharField(max_length=30)),
                ('patient_age', appointment.models.IntegerRangeField()),
                ('patient_sex', models.CharField(max_length=6, choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('patient_email', models.EmailField(max_length=75)),
                ('patient_phone', appointment.models.IntegerRangeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(to='appointment.Patient'),
            preserve_default=True,
        ),
    ]
