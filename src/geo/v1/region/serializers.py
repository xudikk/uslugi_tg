from rest_framework import serializers

from geo.models import Region
from tg.models import Category


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'

