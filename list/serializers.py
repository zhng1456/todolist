# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Thing

#序列化类
class ThingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    task = serializers.CharField(max_length=300)
    complete = serializers.BooleanField(default=False)
    priority = serializers.IntegerField(default=1)  # 新增优先级,数字越大级别越高，默认是1

    def create(self, validated_data):
        return Thing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.task = validated_data.get('task', instance.task)
        instance.complete = validated_data.get('complete', instance.complete)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()
        return instance
