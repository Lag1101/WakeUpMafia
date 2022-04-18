from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_league', views.create_league, name='create_league'),
    path('create_event', views.create_event, name='create_event'),
    path('register', views.register, name='register'),
    path('event/<int:event_id>', views.event, name='event'),
    path('event/<int:event_id>/create_game', views.create_game, name='create_game'),
    path('event/<int:event_id>/generate_game', views.generate_game, name='generate_game'),
    path('event/<int:event_id>/<int:game_id>', views.game_info, name='game_info'),
    path('event/<int:event_id>/<int:game_id>/edit_players', views.game_edit_players, name='game_edit_players'),
    path('event/<int:event_id>/<int:game_id>/edit_results', views.game_edit_results, name='game_edit_results'),
    path('event/<int:event_id>/<int:game_id>/edit_best_move', views.game_edit_best_move, name='game_edit_best_move'),
    path('event/<int:event_id>/<int:game_id>/edit_points', views.game_edit_points, name='game_edit_points'),
    path('rating', views.rating, name='rating'),
]
