# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Thing(models.Model):
    id = models.IntegerField(primary_key=True)#主键
    task = models.CharField(max_length=300)#任务内容
    complete = models.BooleanField(default=False)#是否完成的标志位
