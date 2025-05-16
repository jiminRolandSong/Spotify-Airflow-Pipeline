from django.urls import path
from .views import ArtistStreamsView, PlaylistsView, PlaylistTrackStreamsView

urlpatterns = [
    path('artists/', ArtistStreamsView.as_view(), name='artist-streams'),
    path('playlists/', PlaylistsView.as_view(), name='playlists'),
    path('playlist-tracks/', PlaylistTrackStreamsView.as_view(), name='playlist-tracks'),
]