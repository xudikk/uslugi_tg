from django.db import models

# Create your models here.
from django.db.models import JSONField

from tg import default_log, lang_dict_field


class Log(models.Model):
    user_id = models.BigIntegerField(primary_key=True, null=False)
    messages = models.JSONField(blank=True, null=True)

    def __str__(self):
        return "#%s" % self.user_id


class Languages(models.Model):
    name = JSONField(blank=False, null=False, default=lang_dict_field)
    alias = models.CharField(max_length=32, unique=True)
    sort_order = models.IntegerField(db_index=True, null=True)

    def __str__(self):
        return self.alias





