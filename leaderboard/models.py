from django.db import models
from django.db.models import Sum
from django.db.models import F


class Company(models.Model):
    uid = models.CharField(max_length=128)
    updated = models.DateTimeField(auto_now=True)


class Leader(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=256)

    def category_score(self, category):
      return self.score_set.filter(category=category).aggregate(Sum(F('score')))['score__sum'] or 0

    def closed_score(self):
      return self.category_score('closed')


class Score(models.Model):
    leader = models.ForeignKey(Leader)
    score = models.IntegerField()
    category = models.CharField(max_length=64)
    updated = models.DateTimeField(auto_now=True)
