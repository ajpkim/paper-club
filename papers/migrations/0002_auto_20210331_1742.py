# Generated by Django 3.1.7 on 2021-03-31 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='link',
        ),
        migrations.AddField(
            model_name='paper',
            name='pdf_url',
            field=models.URLField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='paper',
            name='url',
            field=models.URLField(default='', max_length=50),
            preserve_default=False,
        ),
    ]