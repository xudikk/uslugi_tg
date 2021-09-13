from datetime import datetime
from rest_framework import serializers

from base.fields import LangField
from tg.models import Category


class CategorySerializer(serializers.Serializer):
    parent_id = serializers.IntegerField(required=False, )
    name = LangField()
    is_active = serializers.BooleanField(required=False, )
    is_main = serializers.BooleanField(required=False, )
    sort_order = serializers.IntegerField(required=False, )

    def __init__(self, *args, **kwargs):
        self.category_id = kwargs.pop('category')
        super(CategorySerializer, self).__init__(*args, **kwargs)

    def save(self):
        if self.category_id:
            try:
                category_model = Category.objects.get(id=self.category_id)
            except Category.DoesNotExist:
                raise serializers.ValidationError({'category': ['category found region']})
        else:
            category_model = Category()

        parent_id = self.validated_data.get('parent_id', category_model.parent_id)
        name = self.validated_data.get('name', category_model.name)
        is_active = self.validated_data.get('is_active', category_model.is_active)
        is_main = self.validated_data.get('is_main', category_model.is_main)
        sort_order = self.validated_data.get('sort_order', category_model.sort_order)

        category_model.parent_id = parent_id
        category_model.name = name
        category_model.is_active = is_active
        category_model.is_main = is_main
        category_model.sort_order = sort_order
        category_model.save()

        return category_model
