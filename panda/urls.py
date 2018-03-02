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
                url(r'^game/(?P<game_name_slug>[\w\-]+)/make_rating/$', views.make_game_rating, name='game_rating'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/make_comment/$', views.make_game_comment, name='game_comment'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/add_player/$', views.add_player, name='add_player'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/remove_player/$', views.remove_player, name='remove_remove'),

                url(r'^player/(?P<player_name_slug>[\w\-]+)/$', views.show_player, name='show_player'),
                url(r'^player/(?P<player_name_slug>[\w\-]+)/make_rating/$', views.make_player_rating, name='player_rating'),

                url(r'^my_profile/$', views.show_profile, name='my_profile'),
                url(r'^my_profile/register_game/$', views.register_game, name='register_game'),



              ]
