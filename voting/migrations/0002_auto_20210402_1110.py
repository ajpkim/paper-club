# Generated by Django 3.1.7 on 2021-04-02 15:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='vote',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='election',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 4, 11, 10, 7, 47271)),
        ),
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.IntegerField(default=1),
        ),
    ]