from django.urls import path, include


urlpatterns = [
    path('api/v1/', include("tg.api.v1.urls")),

]
