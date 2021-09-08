from rest_framework import serializers

from tg.models import User


class TgUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print("vd", validated_data)
        root = User(**validated_data)
        root.save()
        return root

    class Meta:
        model = User
        fields = '__all__'
