from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=256)

    class Meta:
        fields = ('message',)
