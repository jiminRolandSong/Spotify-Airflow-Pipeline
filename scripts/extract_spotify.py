import spotipy
import os
import json
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pandas as pd
import time


def spotify_api_setup():
    load_dotenv()
    #Authentication
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)
    return sp

def extract_artist_data(sp, artist_ids):
    artists_data = []
    #Get artist info
    for artist_id in artist_ids:
        try:
            artist_info = sp.artist(artist_id)
            
            top_tracks = sp.artist_top_tracks(artist_id)
            
            for track in top_tracks['tracks']:
                track_record = {
                    'artist_id': artist_id,
                    'artist_name': artist_info['name'],
                    'track_name': track['name'],
                    'popularity': track['popularity'],
                    'album': track['album']['name'],
                    'followers': artist_info['followers']['total'],
                    'genres': json.dumps(artist_info['genres']),
                    'extraction_date': datetime.now().strftime('%Y-%m-%d')
                }
                artists_data.append(track_record)
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error extracting data for artist {artist_id}, {e}")
        
    return pd.DataFrame(artists_data)   
            

def extract_playlist_data(sp, playlist_ids):
    playlists_data = []
    playlists_tracks_data = []
    
    for playlist_id in playlist_ids: 
        try:
            playlist_info = sp.playlist(playlist_id)
            
            playlist_record = {
                'playlist_id': playlist_id,
                'playlist_name': playlist_info['name'],
                'owner_id': playlist_info['owner']['id'],
                'followers': playlist_info['followers']['total'] if playlist_info['followers'] else 0,
                'total_tracks': playlist_info['tracks']['total'],
                'extraction_date': datetime.now().strftime('%Y-%m-%d')
            }
            playlists_data.append(playlist_record)
            
            tracks = []
            results = sp.playlist_tracks(playlist_id)
            tracks.extend(results['items'])
            while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])
                time.sleep(0.1)
            
            for item in tracks:
                track = item['track']
                if not track or not track.get('id'):
                    continue
                track_record = {
                    'playlist_id': playlist_id,
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'artist_name': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                    'popularity': track['popularity'],
                    'album': track['album']['name'] if track['album'] else 'Unknown',
                    'duration_ms': track['duration_ms'],
                    'extraction_date': datetime.now().strftime('%Y-%m-%d')
                }
                playlists_tracks_data.append(track_record)
        except Exception as e:
            print(f"Error extracting data for playlist {playlist_id}: {e}")
    
    return pd.DataFrame(playlists_data), pd.DataFrame(playlists_tracks_data)

try:
    sp = spotify_api_setup()  
except Exception as e:
    print(f"Failed to initialize Spotify client: {e}")
    exit(1)

def main():
    
    base_path = os.getenv("AIRFLOW_HOME", os.getcwd())
    # TEST ARTIST STREAMS

    # TripleS, Cutie Sweet
    artist_ids = ["5Z71xE9prhpHrqL5thVMyK", "3PLCOySHJ9zwED5yZvDtPZ"]

    artist_streams_df = extract_artist_data(sp, artist_ids)

    if artist_streams_df.empty:
        print("No artist data extracted. Check artist IDs or Spotify API.")
    else:
        #artist_streams_df.to_csv('artist_streams.csv', index=False)
        artist_streams_df.to_csv(os.path.join(base_path, "artist_streams.csv"), index=False)
        print("Artist Streams DataFrame:")
        print(artist_streams_df.head())

        
    # TEST PLAYLIST STREAMS

    playlist_ids = ["7vhaamErffNetyvUgueBs3", "2wazkzhuzpipWcVKjOa7Vg"]

    playlists_df, playlists_tracks_streams_df = extract_playlist_data(sp, playlist_ids)

    if playlists_df.empty:
        print("No playlist metadata extracted.")
    else:
        #playlists_df.to_csv('playlists.csv', index=False)
        playlists_df.to_csv(os.path.join(base_path, "playlists.csv"), index=False)
        print("Playlists DataFrame:")
        print(playlists_df.head())
        
    if playlists_tracks_streams_df.empty:
        print("No playlist tracks extracted.")
    else:
        #playlists_tracks_streams_df.to_csv('playlists_tracks_streams.csv', index=False)
        playlists_tracks_streams_df.to_csv(os.path.join(base_path, "playlists_tracks_streams.csv"), index=False)
        print("Playlists Tracks Streams DataFrame:")
        print(playlists_tracks_streams_df.head())
    
    

    
    
    

if __name__ == "__main__":
    main()  