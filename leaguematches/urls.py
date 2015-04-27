from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /leaguematches/
    url(r'^$', views.index, name='index'),
    # ex: /leaguematches/season/5/
    url(r'^season/(?P<season_id>[0-9]+)/$', views.season, name='season'),
    # ex: /leaguematches/player/5/
    url(r'^player/(?P<player_id>[0-9]+)/$', views.player, name='player'),
]