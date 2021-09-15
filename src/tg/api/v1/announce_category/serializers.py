from rest_framework import serializers

from tg.models import AnnounceCategories


class AnnounceCtgSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print("vd", validated_data)
        root = AnnounceCategories(**validated_data)
        root.save()
        return root

    class Meta:
        model = AnnounceCategories
        fields = '__all__'
