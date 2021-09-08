from django.db import models
from django.db.models import JSONField

from base.fields import lang_dict_field


class Region(models.Model):
    id = models.AutoField(primary_key=True, null=False, )
    name = JSONField(blank=True, null=True, default=lang_dict_field)
    sort_order = models.IntegerField(db_index=True, null=True)

    def __unicode__(self):
        return self.name['ru']

    def __str__(self):
        return self.name['ru']


class District(models.Model):
    id = models.AutoField(primary_key=True, null=False, )
    name = JSONField(blank=True, null=True, default=lang_dict_field)
    region = models.ForeignKey(Region, related_name="district_region", on_delete=models.CASCADE)
    sort_order = models.IntegerField(db_index=True, null=True)

    @property
    def parent(self):
        return self.region

    def __unicode__(self):
        return self.name['ru']

    def __str__(self):
        return self.name['ru']
