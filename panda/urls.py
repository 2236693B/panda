from django.conf.urls import url
from . import views

urlpatterns = [ url(r'^$', views.index, name='index'),
                url(r'^about/', views.about, name='about'),
                url(r'^games/', views.games, name='games'),
                url(r'^players/', views.players, name='players'),

                url(r'^login/$', views.user_login, name='login'),
                url(r'^sign_up/$', views.sign_up, name='sign_up'),
                url(r'^logout/$', views.user_logout, name='logout'),

                url(r'^game/(?P<game_name_slug>[\w\-]+)/$', views.show_game, name='show_game'),
                url(r'^player/(?P<player_name_slug>[\w\-]+)/$', views.show_player, name='show_player'),



              ]
