from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ArtistStreamSerializer,
    PlaylistSerializer,
    PlaylistTrackStreamSerializer
)
import snowflake.connector
import os
from dotenv import load_dotenv
import json
# Create your views here.

load_dotenv()


def get_snowflake_connection():
    return snowflake.connector.connect(
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                role=os.getenv("SNOWFLAKE_ROLE"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA")
            )

def fetch_data(query):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0].lower() for col in cursor.description]
    rows = cursor.fetchall()
    data = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return data

def process_response(data, serializer_class):
    for item in data:
        if "genres" in item and isinstance(item["genres"], str):
            try:
                item["genres"] = json.loads(item["genres"])
            except:
                item["genres"] = []
    serializer = serializer_class(data=data, many=True)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class ArtistStreamsView(APIView):
    def get(self, request):
        try:
            query = """
                    SELECT artist_id, artist_name, track_name, popularity, album,
                    followers, genres, extraction_date, popularity_category,
                        is_kpop, is_jpop, processed_at
                    FROM artist_streams
                    ORDER BY processed_at DESC
                    LIMIT 50
                """
            data = fetch_data(query)
            return process_response(data, ArtistStreamSerializer)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PlaylistsView(APIView):
    def get(self, request):
        try:
            query = """
                SELECT playlist_id, playlist_name, owner_id, followers,
                       total_tracks, extraction_date, processed_at
                FROM playlists
                ORDER BY processed_at DESC
                LIMIT 50
            """
            data = fetch_data(query)
            return process_response(data, PlaylistSerializer)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PlaylistTrackStreamsView(APIView):
    def get(self, request):
        try:
            query = """
                SELECT playlist_id, track_id, track_name, artist_name,
                       popularity, album, duration_ms, extraction_date,
                       duration_min, processed_at
                FROM playlist_streams
                ORDER BY processed_at DESC
                LIMIT 50
            """
            data = fetch_data(query)
            return process_response(data, PlaylistTrackStreamSerializer)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
