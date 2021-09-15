from django.urls import path

from tg.api.v1.announce.views import AnnounceView
from tg.api.v1.announce_category.views import AnnounceCatView
from tg.api.v1.log.views import UserLogView
from tg.api.v1.user.views import UserView

urlpatterns = [
    path('log/<int:user_id>/', UserLogView.as_view(), name='user_log'),
    path('user/<int:user_id>/', UserView.as_view(), name='tg_user'),
    path('user/', UserView.as_view(), name='tg_user'),
    path('announce/', AnnounceView.as_view(), name='tg_announce'),
    path('announce/<int:user_id>/', AnnounceView.as_view(), name='tg_announce'),
    path('announce_cat/', AnnounceCatView.as_view(), name='tg_cat_announce'),

]
