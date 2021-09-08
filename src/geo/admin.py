from django.contrib import admin

from .models import Region, District


class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
