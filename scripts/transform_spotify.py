import pandas as pd
import json
import os
from datetime import datetime

def clean_artist_data(df):
    if df.empty:
        print("Artist DataFrame is Empty")
        return df
    
    cleaned_df = df.copy()
    
    # Missing values
    cleaned_df = df.dropna(subset=['artist_name', 'track_name'])
    
    # Standardize data types
    cleaned_df['popularity'] = df['popularity'].astype(int, errors='ignore')
    cleaned_df['followers'] = df['followers'].astype(int, errors='ignore')
    
    # Parse genres
    cleaned_df['genres'] = cleaned_df['genres'].apply(lambda x: json.loads(x) if isinstance(x, str) else [])
    
    # Add derived columns
    cleaned_df['popularity_category'] = pd.cut(
        cleaned_df['popularity'],
        bins=[0, 30, 60, 100],
        labels=['Low', 'Medium', 'High']
    )
    cleaned_df['is_kpop'] = cleaned_df['genres'].apply(lambda x: 'k-pop' in [g.lower() for g in x])
    cleaned_df['is_jpop'] = cleaned_df['genres'].apply(lambda x: 'j-pop' in [g.lower() for g in x])
    
    cleaned_df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return cleaned_df

def clean_playlists_data(df):
    if df.empty:
        print("Playlists DataFrame is empty. Skipping cleaning.")
        return df
    
    cleaned_df = df.copy()
    
    cleaned_df['followers'] = cleaned_df['followers'].fillna(0).astype(int)
    cleaned_df['total_tracks'] = cleaned_df['total_tracks'].fillna(0).astype(int)
    
    cleaned_df = cleaned_df.drop_duplicates(subset=['playlist_id'])
      
    cleaned_df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      
    return cleaned_df

def clean_tracks_data(df):
    if df.empty:
        print("Playlist Tracks DataFrame is empty. Skipping cleaning.")
        return df
    
    cleaned_df = df.copy()
    
    cleaned_df = cleaned_df.dropna(subset=['track_name', 'artist_name'])
    
    cleaned_df['popularity'] = cleaned_df['popularity'].fillna(0).astype(int)
    cleaned_df['duration_ms'] = cleaned_df['duration_ms'].fillna(0).astype(int)
    
    cleaned_df['duration_min'] = round(cleaned_df['duration_ms'] / 60000, 2)
    
    cleaned_df = cleaned_df.drop_duplicates(subset=['playlist_id', 'track_id'])
    
    cleaned_df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return cleaned_df


def main():
    base_path = os.getenv("AIRFLOW_HOME", os.getcwd())

    # CLEAN ARTISTS DATA
    artist_streams_df = pd.read_csv(os.path.join(base_path, 'artist_streams.csv'))
    artist_streams_df = clean_artist_data(artist_streams_df)
    artist_streams_df.to_csv(os.path.join(base_path, 'cleaned_artist_streams.csv'), index=False)

    print("Cleaned Artist Streams:")
    print(artist_streams_df.head())

    # CLEAN PLAYLIST DATA
    playlists_df = pd.read_csv(os.path.join(base_path, 'playlists.csv'))
    playlists_df = clean_playlists_data(playlists_df)
    playlists_df.to_csv(os.path.join(base_path, 'cleaned_playlists.csv'), index=False)

    print("\nCleaned Playlists:")
    print(playlists_df.head())

    # CLEAN PLAYLIST TRACKS
    playlist_tracks_df = pd.read_csv(os.path.join(base_path, 'playlists_tracks_streams.csv'))
    playlist_tracks_df = clean_tracks_data(playlist_tracks_df)
    playlist_tracks_df.to_csv(os.path.join(base_path, 'cleaned_playlists_tracks_streams.csv'), index=False)

    print("\nCleaned Playlist Tracks Streams:")
    print(playlist_tracks_df.head())

if __name__ == "__main__":
    main()