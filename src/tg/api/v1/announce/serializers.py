from rest_framework import serializers

from tg.models import Announce


class AnnounceSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print("vd", validated_data)
        root = Announce(**validated_data)
        root.save()
        return root

    class Meta:
        model = Announce
        fields = '__all__'
