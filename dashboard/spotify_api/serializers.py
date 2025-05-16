from rest_framework import serializers

class ArtistStreamSerializer(serializers.Serializer):
    artist_id = serializers.CharField()
    artist_name = serializers.CharField()
    track_name = serializers.CharField()
    popularity = serializers.IntegerField()
    album = serializers.CharField()
    followers = serializers.IntegerField()
    genres = serializers.ListField()
    extraction_date = serializers.CharField()
    popularity_category = serializers.CharField()
    is_kpop = serializers.BooleanField()
    is_jpop = serializers.BooleanField()
    processed_at = serializers.CharField()

class PlaylistSerializer(serializers.Serializer):
    playlist_id = serializers.CharField()
    playlist_name = serializers.CharField()
    owner_id = serializers.CharField()
    followers = serializers.IntegerField()
    total_tracks = serializers.IntegerField()
    extraction_date = serializers.CharField()
    processed_at = serializers.CharField()

class PlaylistTrackStreamSerializer(serializers.Serializer):
    playlist_id = serializers.CharField()
    track_id = serializers.CharField()
    track_name = serializers.CharField()
    artist_name = serializers.CharField()
    popularity = serializers.IntegerField()
    album = serializers.CharField()
    duration_ms = serializers.IntegerField()
    extraction_date = serializers.CharField()
    duration_min = serializers.FloatField()
    processed_at = serializers.CharField()

