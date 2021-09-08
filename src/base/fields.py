from __future__ import unicode_literals
from rest_framework import serializers

def lang_dict_field():
    return {'ru': '', 'uz': ''}

def default_salary():
    return {"from": 0, "to": 0}

class LangField(serializers.Serializer):
    uz = serializers.CharField(max_length=150, required=True)
    ru = serializers.CharField(max_length=150, required=True)
