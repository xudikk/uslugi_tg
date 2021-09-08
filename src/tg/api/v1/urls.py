from django.urls import path

from tg.api.v1.log.views import UserLogView
from tg.api.v1.user.views import UserView

urlpatterns = [
    path('log/<int:user_id>/', UserLogView.as_view(), name='user_log'),
    path('user/<int:user_id>/', UserView.as_view(), name='tg_user'),
    path('user/', UserView.as_view(), name='tg_user'),

]
