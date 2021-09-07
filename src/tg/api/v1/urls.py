from django.urls import path

from .language.views import LanguagesView


urlpatterns = [

    path('languages/', LanguagesView.as_view(), name='hr-language-list'),
    path('languages/<int:pk>/', LanguagesView.as_view(), name='hr-language-one'),

]
