from rest_framework import serializers
from models import Thing


class ThingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    task = serializers.CharField(max_length=300)
    complete = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Thing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.task = validated_data.get('task', instance.task)
        instance.complete = validated_data.get('complete', instance.complete)
        instance.save()
        return instance
