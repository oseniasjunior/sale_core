from rest_framework import serializers


class GetByNameSerializerParam(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=64)
