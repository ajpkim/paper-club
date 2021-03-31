from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

class Paper(models.Model):
    url = models.URLField(max_length=50)
    pdf_url = models.URLField(max_length=50, default="")
    title = models.CharField(max_length=500)
    authors = models.ManyToManyField('Author', through='PaperAuthor')
    abstract = models.CharField(max_length=1000)
    key_words = models.ManyToManyField('KeyWord', through='PaperKeyWord')
    pub_date = models.DateField()

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=50)
    papers = models.ManyToManyField('Paper', through='PaperAuthor')

    def  __str__(self):
        return self.name


class PaperAuthor(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def  __str__(self):
        return f'Authorship: {self.author} ---> {self.paper}'

class KeyWord(models.Model):
    key_word = models.CharField(max_length=30)

    def  __str__(self):
        return self.key_word


class PaperKeyWord(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    key_word = models.ForeignKey(KeyWord, on_delete=models.CASCADE)

    def  __str__(self):
        return f'{self.key_word} ---> {self.paper}'


# TODO: Create Club model in the Clubs app
# class Proposal(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
#     group = models.ForeignKey(Club, on_delete=models.SET_NULL)
#     create_time = models.DateTimeField(auto_now_add=True)

    # def  __str__(self):
    #     return f'Proposal: {self.username} ---> {self.title}'
