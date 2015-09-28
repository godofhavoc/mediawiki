from django.db import models

class QueryLinks(models.Model):
    title = models.CharField(max_length=50)
    count = models.IntegerField()
