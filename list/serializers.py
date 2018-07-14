# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Thing

#序列化类
class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thing
        fields = ('id', 'task', 'complete', 'priority')
