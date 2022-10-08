from django.urls import path,  include
from . import views
urlpatterns = [
    path('', views.loginUser, name='login'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('video_player/', views.video_view, name='video_player'),

    # Watch list urls
    path('addvideotowatchlist/', views.add_to_watchlist, name='addvideotowatchlist'),
    path('watchlist/', views.watch_list_view, name='watchlist'),
    path('deletewatchlist/', views.delete_watchlist_video, name='deletewatchlist'),
    

    path('channelhome/', views.channel_home_view, name='channelhome'),
    path('search/', views.search_view, name='search'),

    path('auto_complete/', views.auto_complete, name='auto_complete'),
    # Add data on home page on load using ajax
    path('add_data_home_onload/', views.add_data_home_onload, name='add_data_home_onload'),
    # Update data in db
    path('update_data_db/', views.update_data_db, name='update_data_db'),

    # Update data in home page AJAX
    path('update_data_home_ajax/', views.home_data_ajax, name='update_data_home_ajax'),
    # Update data in home page recent tab AJAX
    path('update_data_recent_ajax/', views.home_data_recent_ajax, name='update_data_home_recent_ajax'),

    #Filter Videos in home page AJAX
    path('filter_videos_home/', views.filter_videos_home, name='filter_videos_home'),

    #Follow a personality
    path('follow_personality_home/', views.follow_personality, name='follow_personality_home'),
    path('follow_personality/', views.follow_personality_ajax, name='follow_personality'),
    path('unfollow_personality/', views.unfollow_personality_ajax, name='unfollow_personality'),
    

    #  Athletes profile
    path('follow_athletes/', views.all_profiles_view, name='follow_athletes'),
    path('athlete_profile/', views.athlete_profile, name='athlete_profile'),

    # Follow an athlete AJAX
    path('follow_athlete_ajax_call/', views.follow_athlete_ajax, name='follow_athlete_ajax_call'),
    # unFollow an athlete AJAX
    path('unfollow_athlete_ajax_call/', views.unfollow_athlete_ajax, name='unfollow_athlete_ajax_call'),

    # Community  
    path('community/', views.community, name='community'),
    path('community_profile/', views.community_profile, name='community_profile'),

    # Follow an athlete AJAX
    path('follow_community_ajax_call/', views.follow_community_ajax_call, name='follow_community_ajax_call'),
    # unFollow an athlete AJAX
    path('unfollow_community_ajax_call/', views.unfollow_community_ajax_call, name='unfollow_community_ajax_call'),


    # for testing purposes
    path('test/', views.test, name='test'),

    # blocking video
    path('block_video/<str:id>/', views.block_video, name="block_video")
    
   
]
