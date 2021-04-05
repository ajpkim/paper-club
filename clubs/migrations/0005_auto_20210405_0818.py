# Generated by Django 3.1.7 on 2021-04-05 12:18

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0001_initial'),
        ('clubs', '0004_auto_20210405_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 7, 12, 18, 52, 323387, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='election',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='papers.paper'),
        ),
    ]
