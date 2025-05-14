import pandas as pd 
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

BASE_DIR = "/home/aangava/MSP/airflow"

print(f"[DEBUG] BASE_DIR is: {BASE_DIR}")
print(f"[DEBUG] Reading file: {os.path.join(BASE_DIR, 'cleaned_artist_streams.csv')}")


conn_params = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA")
}

def snowflake_connection():
    try:
        print(pd.__version__)
        df = pd.DataFrame({"test": [1, 2, 3]})
        print(df)
        conn = conn = snowflake.connector.connect(**conn_params)
        print("Connected to Snowflake successfully.")
        return conn
    except Exception as e:
        print(f"Failed to connect to Snowflake: {e}")
        return None
    
def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        print("Query executed")
    except Exception as e:
        print(f"Query failed: {e}")

def create_database_and_schema(conn):
    queries = [
        f"CREATE DATABASE IF NOT EXISTS {conn_params['database']}",
        f"USE DATABASE {conn_params['database']}",
        f"CREATE SCHEMA IF NOT EXISTS {conn_params['schema']}",
        f"USE SCHEMA {conn_params['schema']}"
    ]
    for query in queries:
        execute_query(conn, query)
        
def create_tables(conn):
    # Artist Streams table
    cursor = conn.cursor()
    cursor.execute(f"USE DATABASE {conn_params['database']}")
    cursor.execute(f"USE SCHEMA {conn_params['schema']}")
    
    artist_table_query = """
    CREATE TABLE IF NOT EXISTS artist_streams (
        artist_id STRING,
        artist_name STRING,
        track_name STRING,
        popularity INTEGER,
        album STRING,
        followers INTEGER,
        genres ARRAY,
        extraction_date STRING,
        popularity_category STRING,
        is_kpop BOOLEAN,
        is_jpop BOOLEAN,
        processed_at STRING
    )
    """
    # Playlists table
    playlists_table_query = """
    CREATE TABLE IF NOT EXISTS playlists (
        playlist_id STRING,
        playlist_name STRING,
        owner_id STRING,
        followers INTEGER,
        total_tracks INTEGER,
        extraction_date STRING,
        processed_at STRING
    )
    """
    # Playlist Tracks table
    playlist_tracks_table_query = """
    CREATE TABLE IF NOT EXISTS playlist_streams (
        playlist_id STRING,
        track_id STRING,
        track_name STRING,
        artist_name STRING,
        popularity INTEGER,
        album STRING,
        duration_ms INTEGER,
        extraction_date STRING,
        duration_min FLOAT,
        processed_at STRING
    )
    """
    for query in [artist_table_query, playlists_table_query, playlist_tracks_table_query]:
        execute_query(conn, query)

def load_csv_to_snowflake(conn, csv_path, table_name):
    try:
        
        # Check if CSV exists
        if not os.path.exists(csv_path):
            print(f"{csv_path} not found. Skipping.")
            return
        
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Handle genres for artist_streams (convert to JSON string)
        if table_name == "artist_streams":
            df['genres'] = df['genres'].apply(lambda x: json.dumps(eval(x)) if isinstance(x, str) else json.dumps(x))
        
        # Convert DataFrame to list of tuples
        records = [tuple(x) for x in df.to_numpy()]
        
        df.columns = [col.upper() for col in df.columns]
        
        
        success, nchunks, nrows, _ = write_pandas(conn=conn,
        df=df,
        table_name=table_name,
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )
        print(f"Loaded {nrows} rows into {table_name} successfully.")

    except Exception as e:
        print(f"Failed to load {csv_path} into {table_name}: {e}")
        
def main():
    conn = snowflake_connection()
    
    if not conn:
        return
    
    try:
        create_database_and_schema(conn)
        
        create_tables(conn)
        
        load_csv_to_snowflake(conn, os.path.join(BASE_DIR, 'cleaned_artist_streams.csv'), 'ARTIST_STREAMS')
        load_csv_to_snowflake(conn, os.path.join(BASE_DIR, 'cleaned_playlists.csv'), 'PLAYLISTS')
        load_csv_to_snowflake(conn, os.path.join(BASE_DIR, 'cleaned_playlists_tracks_streams.csv'), 'PLAYLIST_STREAMS')
        
        cursor = conn.cursor()
        for table in ['artist_streams', 'playlists', 'playlist_streams']:
            cursor.execute(f"SELECT * FROM {table} LIMIT 5")
            print(f"\nSample from {table}:")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        cursor.close()
    
    finally:
        conn.close()
        print("Snowflake connection closed.")

if __name__ == "__main__":
    main()