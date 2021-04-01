# Generated by Django 3.1.7 on 2021-04-01 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0003_auto_20210331_2330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paper',
            old_name='pub_date',
            new_name='published',
        ),
        migrations.AddField(
            model_name='paper',
            name='arxiv_id',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paper',
            name='pdf_url',
            field=models.URLField(max_length=50),
        ),
    ]
