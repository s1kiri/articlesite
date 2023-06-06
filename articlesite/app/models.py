from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # name = models.CharField(max_length=20, default='@')
    # surname = models.CharField(max_length=50, default='@')
    # email = models.CharField(max_length=50, default='@', unique=True)
    # password = models.CharField(max_length=20, default='@')
    # REQUIRED_FIELDS = ['name', 'surname', 'email', 'password']
    def __str__(self):
        return self.username
    class Meta:
        unique_together = ('username',)

class category(models.Model):
    cat_name = models.CharField(max_length=100)
    describe = models.CharField(max_length=1000)

class articles(models.Model):
    cat = models.ForeignKey(category,on_delete=models.RESTRICT)
    text = models.TextField(max_length=50000)
    title = models.CharField(max_length=500)
    author_id = models.IntegerField()

class statuses(models.Model):
    status = models.CharField(max_length=70)

class article_status(models.Model):
    user_id = models.ForeignKey('app.User', on_delete=models.RESTRICT)
    article_id = models.ForeignKey(articles, on_delete=models.RESTRICT)
    status_id = models.ForeignKey(statuses, on_delete=models.RESTRICT)

class reviews(models.Model):
    article_id = models.ForeignKey(articles, on_delete=models.RESTRICT)
    reviewer_id = models.IntegerField()
    text = models.TextField(max_length=3000, default='')