from django.urls import path, include


urlpatterns = [
    path('api/v1/', include("tg.api.v1.urls")),
    path('api/v1/g/', include("geo.v1.urls")),


]
