from rest_framework import serializers
from core import models


class StateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=64)
    abbreviation = serializers.CharField(required=True, max_length=2)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    active = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        if not self.partial:
            if not attrs.get('abbreviation').isupper():
                raise Exception('O campo sigla dever ser maiusculo')
        return super(StateSerializer, self).validate(attrs)

    def create(self, validated_data):
        return models.State.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

    def to_representation(self, instance):
        result = super(StateSerializer, self).to_representation(instance)
        result['campo_teste'] = 'Eu sou um campo apenas de teste'
        return result
