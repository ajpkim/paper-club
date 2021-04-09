import random

from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()


class Paper(models.Model):
    url = models.URLField(max_length=50)
    pdf_url = models.URLField(max_length=50)
    arxiv_id = models.CharField(max_length=20)
    title = models.CharField(max_length=500)
    authors = models.ManyToManyField('Author', through='AuthorPaper')
    abstract = models.CharField(max_length=5000)
    key_words = models.ManyToManyField('KeyWord', through='KeyWordPaper')
    published = models.DateField()

    def __str__(self):
        return self.title

    
class Author(models.Model):
    name = models.CharField(max_length=50)
    papers = models.ManyToManyField('Paper', through='AuthorPaper')

    def  __str__(self):
        return self.name


class AuthorPaper(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    def  __str__(self):
        return f'{self.author}: {self.paper}'

class KeyWord(models.Model):
    key_word = models.CharField(max_length=30)

    def  __str__(self):
        return self.key_word


class KeyWordPaper(models.Model):
    key_word = models.ForeignKey(KeyWord, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    def  __str__(self):
        return f'{self.key_word}: {self.paper}'
