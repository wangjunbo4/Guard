'''
Author: Gtylcara.
Date: 2021-02-21 12:11:11
LastEditors: Gtylcara.
LastEditTime: 2021-03-15 19:24:40
'''
from django.db import models
from django.db.models.fields import IntegerField

class UserDB(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class DataDB(models.Model):
    name = models.CharField(max_length=20)
    status = models.IntegerField(default=0)
    working = models.IntegerField(default=0)
    power = models.IntegerField(default=100)


class LogDB(models.Model):
    name = models.CharField(max_length=20)
    status = models.IntegerField(default=0)
    time = models.CharField(max_length=20)
    

# from Guard import models
# models.DataDB.objects.create(name="1", status=1, power=100)
