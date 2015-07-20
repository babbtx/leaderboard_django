from django.db import models

class Company(models.Model):
    uid = models.CharField(max_length=128)
    updated = models.DateTimeField(auto_now=True)

class Leader(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=256)

class Score(models.Model):
    leader = models.ForeignKey(Leader)
    score = models.IntegerField()
    category = models.CharField(max_length=64)
    updated = models.DateTimeField(auto_now=True)
