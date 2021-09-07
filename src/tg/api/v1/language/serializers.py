from rest_framework import serializers

from yesboss.hr.models import Languages


class LanguageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        course = Languages(**validated_data)
        course.save()
        return course

    class Meta:
        model = Languages
        fields = '__all__'

