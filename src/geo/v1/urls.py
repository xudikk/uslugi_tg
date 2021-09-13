from django.urls import path

from tg.api.v1.category.views import CategoryView
from .region.views import RegionView
from .district.views import DistrictView

urlpatterns = [
    path('regions/', RegionView.as_view(), name='geo-region-list'),
    path('regions/<int:pk>/', RegionView.as_view(), name='geo-region-one'),
    path('regions/<name>/', RegionView.as_view(), name='geo-region-one'),

    path('category/', CategoryView.as_view(), name='category-list'),
    path('category/<slug>/', CategoryView.as_view(), name='category-one'),


    path('districts/', DistrictView.as_view(), name='geo-district-list'),
    path('districts/<int:pk>/', DistrictView.as_view(), name='geo-district-one'),
]
