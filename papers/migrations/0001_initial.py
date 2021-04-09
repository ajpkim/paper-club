# Generated by Django 3.2 on 2021-04-09 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AuthorPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.author')),
            ],
        ),
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_word', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='KeyWordPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.keyword')),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=50)),
                ('pdf_url', models.URLField(max_length=50)),
                ('arxiv_id', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=500)),
                ('abstract', models.CharField(max_length=1000)),
                ('published', models.DateField()),
                ('authors', models.ManyToManyField(through='papers.AuthorPaper', to='papers.Author')),
                ('key_words', models.ManyToManyField(through='papers.KeyWordPaper', to='papers.KeyWord')),
            ],
        ),
        migrations.AddField(
            model_name='keywordpaper',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.paper'),
        ),
        migrations.AddField(
            model_name='authorpaper',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.paper'),
        ),
        migrations.AddField(
            model_name='author',
            name='papers',
            field=models.ManyToManyField(through='papers.AuthorPaper', to='papers.Paper'),
        ),
    ]
