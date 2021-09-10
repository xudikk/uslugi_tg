from django.urls import path

from .region.views import RegionView
from .district.views import DistrictView

urlpatterns = [
    path('regions/', RegionView.as_view(), name='geo-region-list'),
    path('regions/<int:pk>/', RegionView.as_view(), name='geo-region-one'),
    path('regions/<name>/', RegionView.as_view(), name='geo-region-one'),

    path('districts/', DistrictView.as_view(), name='geo-district-list'),
    path('districts/<int:pk>/', DistrictView.as_view(), name='geo-district-one'),
]
