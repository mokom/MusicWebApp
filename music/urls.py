from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Uploads urls
    path('upload/album', views.create_album, name='upload_album'),
    path('upload/single', views.create_track, name='upload_single'),
    # Track urls
    path('track/<slug>', views.track_detail, name='track_detail'),
    path('track/<slug>/edit', views.edit_track, name='edit_track'),
    path('track/<slug>/favorite/', views.favorite_track, name='favorite_track'),
    path('track/<slug>/delete', views.delete_track, name='delete_track'),
    path('track/<slug:slug>/like', views.track_like, name='like_track'),

    # Album urls
    path('albums/', views.album_list, name='album_list'),
    path('album/<slug>', views.album_detail, name='album_detail'),
    path('album/<slug>/upload', views.create_track_album, name='add_to_album'),
    path('album/<slug>/edit', views.edit_album, name='edit_album'),
    path('album/<slug>/delete', views.delete_album, name='delete_album'),
    path('album/<slug>/favorite_album/', views.favorite_album, name='favorite_album'),


#     Playlist Urls
    path('playlists/', views.ManagePlaylistListView.as_view(), name='manage_playlist_list'),
    path('playlists/create/', views.PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlists/<int:pk>/edit/', views.PlaylistUpdateView.as_view(), name='playlist_edit'),
    path('playlists/<int:pk>/delete/', views.PlaylistDeleteView.as_view(), name='playlist_delete'),
    path('playlist/add/<int:track>/<int:playlist>/', views.AddToPlaylist.as_view(), name='add_music_to_playlist'),
    path('playlist/remove/<int:track>/<int:playlist>/', views.RemoveFromPlaylist.as_view(),
         name='remove_music_from_playlist'),
    path('playlist/<slug:slug>/', views.PlaylistDetail.as_view(), name='playlist_detail'),
]