from django.conf.urls import url
from . import views

urlpatterns = [ url(r'^$', views.index, name='index'),
                url(r'^about/', views.about, name='about'),
                url(r'^games/', views.games, name='games'),
                url(r'^contact_us/', views.contact_us, name = "contact_us"),
				url(r'^players/', views.players, name='players'),
                url(r'report/(?P<player_name_slug>[\w\-]+)/$', views.report_player, name='report_player'),

                url(r'^login/$', views.user_login, name='login'),
                url(r'^sign_up/$', views.sign_up, name='sign_up'),
                url(r'^studio_sign_up/$', views.studio_sign_up, name='studio_sign_up'),
                url(r'^logout/$', views.user_logout, name='logout'),

                url(r'^game/(?P<game_name_slug>[\w\-]+)/$', views.show_game, name='show_game'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/make_rating/$', views.make_game_rating, name='game_rating'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/make_comment/$', views.make_game_comment, name='game_comment'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/add_player/$', views.add_player, name='add_player'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/remove_player/$', views.remove_player, name='remove_player'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/edit_game_profile/$', views.edit_game_profile, name='edit_game_profile'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/delete_game_profile/$', views.delete_game_profile, name='delete_game_profile'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/(?P<comment_id>\d+)/delete_comment/$', views.delete_game_comment, name='delete_game_comment'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/(?P<comment_id>\d+)/edit_comment/$', views.edit_game_comment, name='edit_game_comment'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/players$', views.get_game_players, name='Player_AJAX'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/recommend$', views.recommend_game, name='Recommend_game'),
                url(r'^game/(?P<game_name_slug>[\w\-]+)/update/$', views.update_game, name='update_game'),
                url(r'^reset/$', views.reset, name='Reset'),


                url(r'^player/(?P<player_name_slug>[\w\-]+)/$', views.show_player, name='show_player'),
                url(r'^player/(?P<player_name_slug>[\w\-]+)/make_rating/$', views.make_player_rating, name='player_rating'),

                url(r'^studio/(?P<studio_name_slug>[\w\-]+)/$', views.show_studio, name='show_studio'),

                url(r'^search/games', views.games_search, name='games_search'),
                url(r'^search/players', views.player_search, name='player_search'),

                url(r'^my_profile/$', views.show_profile, name='my_profile'),
                url(r'^my_profile/register_game/$', views.register_game, name='register_game'),
                url(r'^my_profile/edit_player_profile/$', views.edit_player_profile, name='edit_player_profile'),
                url(r'^my_profile/edit_studio_profile/$', views.edit_studio_profile, name='edit_studio_profile'),
                url(r'^my_profile/delete_profile/$', views.delete_profile, name='delete_profile'),
                url(r'^my_profile/approve/$', views.approve_player, name='approve_my_profile'),




                url(r'forum_dashboard/$', views.DashboardView.as_view(), name="forum_dashboard"),

                url(r'^forum/', views.TopicList.as_view(), name="topic_list"),
                url(r'^forum/topic/add/$', views.TopicAdd.as_view(), name="new_topic"),
                url(r'^forum/topic/view/(?P<slug>[-\w]+)/$', views.TopicView.as_view(), name="view_topic"),
                url(r'^forum/topic/votes/(?P<slug>[-\w]+)/up/$', views.TopicVoteUpView.as_view(), name="topic_vote_up"),
                url(r'^forum/topic/votes/(?P<slug>[-\w]+)/down/$', views.TopicVoteDownView.as_view(), name="topic_vote_down"),

                url(r'^comment/delete/(?P<comment_id>[-\w]+)/$',
                    views.ForumCommentDelete.as_view(), name="comment_delete"),
                

                url(r'^forum/categories/$', views.ForumCategoryList.as_view(), name="forum_categories"),
                url(r'^forum/category/(?P<slug>[-\w]+)/$', views.ForumCategoryView.as_view(), name="forum_category_detail"),

                url(r'^comment/add/$', views.ForumCommentAdd.as_view(), name="new_comment"),
                url(r'^comment/votes/(?P<pk>[-\w]+)/up/$', views.CommentVoteUpView.as_view(), name="comment_vote_up"),
                url(r'^comment/votes/(?P<pk>[-\w]+)/down/$', views.CommentVoteDownView.as_view(), name="comment_vote_down"),

                url(r'^forum_dashboard/category/list/$', views.CategoryList.as_view(), name="categories"),
                url(r'^forum_dashboard/category/add/$', views.CategoryAdd.as_view(), name="add_category"),
                url(r'^forum_dashboard/category/delete/(?P<slug>[-\w]+)/$',
                    views.CategoryDelete.as_view(), name="delete_category"),
                url(r'^forum_dashboard/category/edit/(?P<slug>[-\w]+)/$',
                    views.CategoryEdit.as_view(), name="edit_category"),
                url(r'^forum_dashboard/category/view/(?P<slug>[-\w]+)/$',
                    views.CategoryDetailView.as_view(), name="view_category"),

                url(r'^forum_dashboard/topics/list/$', views.DashboardTopicList.as_view(), name="topics"),
                url(r'^forum_dashboard/topics/delete/(?P<slug>[-\w]+)/$', views.TopicDeleteView.as_view(), name="delete_topic"),
                url(r'^forum_dashboard/topic/view/(?P<slug>[-\w]+)/$', views.TopicDetail.as_view(), name="topic_detail"),
                url(r'^forum_dashboard/topic/status/(?P<slug>[-\w]+)/$', views.TopicStatus.as_view(), name="topic_status"),

                

                url(r'^register/$', views.ForumIndexView.as_view(), name="signup"),


                   
                url(r'^googleb00694232a77d6d0.html$', views.google_veri, name='google_veri'),
                url(r'^sitemap/$', views.sitemap, name='sitemap'),
              ]

