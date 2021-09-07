from rest_framework import serializers

from yesboss.tg.models import Log


class UserLogSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        root = Log(**validated_data)
        root.save()
        return root

    class Meta:
        model = Log
        fields = '__all__'
