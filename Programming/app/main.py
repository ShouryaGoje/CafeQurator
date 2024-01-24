from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token
  

def get_auth_header(token):
    return {"Authorization":"Bearer "+token}


def search_for_artist(token,artist_name):
    url="https://api.spotify.com/v1/search"
    headers=get_auth_header(token)

    query=f"?q={artist_name}&type=artist&limit=1"

    query_url=url+query
    result=get(query_url,headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result)==0:
        print("No artist")
        return None
    return json_result[0]    


def get_songs_by_artist(token,artist_id):
    url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=IN"
    headers=get_auth_header(token)
    result=get(url,headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result





def get_all_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)

    params = {
        'country': 'IN',
        'limit': 50  # Maximum limit per request
    }

    all_songs = []

    while True:
        try:
            result = get(url, headers=headers, params=params)
            result.raise_for_status()
            json_result = result.json()["tracks"]

            if not json_result:
                break  # No more tracks

            all_songs.extend(json_result)

            # Move to the next page if available
            if 'next' in result.json():
                url = result.json()['next']
            else:
                break  # No more pages

        except Exception as e:
            print(f"Error getting top tracks: {e}")
            break

    return all_songs

# Usage
token = get_token()
#songs=get_songs_by_artist(token,artist_id)
# for idx,song in enumerate(songs):
#     print(f"{idx+1}.{song['name']}")

if token:
    result = search_for_artist(token, "Arijit Singh")

    if result:
        artist_id = result["id"]
        all_songs = get_all_songs_by_artist(token, artist_id)

        if all_songs:
            for idx, song in enumerate(all_songs):
                print(f"{idx + 1}. {song['name']}")
        else:
            print("No songs found for the artist.")
else:
    print("Token retrieval failed.")




