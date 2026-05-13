import os
from dotenv import load_dotenv
import requests as req
import json
from src.utils import get_api_key

load_dotenv()
base_url = os.getenv("BASE_URL")



def get_channel_statistics(channel_id):
    params = {
        "part": "snippet,statistics",
        "id": channel_id
    }

    res = req.get(f"{base_url}/channels", params=params | {"key": get_api_key()}).json()

    items = res.get("items", [])
    if not items:
        return None

    item = items[0]

    snippet = item.get("snippet", {})
    statistics = item.get("statistics", {})

    channel_data = {
        "channelId": item.get("id"),
        "channelTitle": snippet.get("title"),
        "publishedAt": snippet.get("publishedAt"),
        "subscriberCount": statistics.get("subscriberCount"),
        "viewCount": statistics.get("viewCount"),
        "videoCount": statistics.get("videoCount")
    }

    return channel_data

def get_playlist_id(handle):
    params = {
    "part": "contentDetails",
    "forHandle": handle
    }
    res = req.get(f"{base_url}/channels",params=params | {"key": get_api_key()}).json()

    return res['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def get_all_video_ids(playlistId):
    video_ids = []
    next_page_token = None

    while True:
        params = {
            "part": "contentDetails",
            "playlistId": playlistId,
            "maxResults": 50,
            "pageToken": next_page_token
        }

        # Appel API
        response = req.get(f"{base_url}/playlistItems", params=params | {"key": get_api_key()})
        data = response.json()

        # Extraction des IDs dans la page actuelle
        items = data.get('items', [])
        for item in items:
            video_ids.append(item['contentDetails']['videoId'])

        # On vérifie s'il y a une page suivante
        next_page_token = data.get('nextPageToken')

        # Si pas de token, on a fini !
        if not next_page_token:
            break
    print(f"Total video ids fetched: {len(video_ids)}")
    return video_ids


def get_videos_data_batch(video_ids_list):

    ids_string = ",".join(video_ids_list)

    params = {
        "part": "snippet,contentDetails,statistics,topicDetails",
        "id": ids_string
    }

    res = req.get(f"{base_url}/videos", params=params | {"key": get_api_key()}).json()

    batch_data = []

    # On boucle sur les vidéos renvoyées dans ce batch
    for item in res.get("items", []):
        snippet = item.get("snippet", {})
        contentDetails = item.get("contentDetails", {})
        statistics = item.get("statistics", {})
        topicDetails = item.get("topicDetails", {})

        video_data = {
            "videoId": item.get("id"),
            "title": snippet.get("title"),
            "publishedAt": snippet.get("publishedAt"),
            "duration": contentDetails.get("duration"),
            "viewCount": statistics.get("viewCount"),
            "likeCount": statistics.get("likeCount"),
            "commentCount": statistics.get("commentCount"),
            "thumbnailUrl": snippet.get("thumbnails", {}).get("medium", {}).get("url"),
            "topicCategories": topicDetails.get("topicCategories", [])
        }
        batch_data.append(video_data)

    return batch_data

def get_all_videos_dataset(all_videos_ids):
    final_dataset = []

    for i in range(0, len(all_videos_ids), 50):
        print(f"Batch {int(i/50 + 1)}")
        batch_ids = all_videos_ids[i:i+50]

        batch_data = get_videos_data_batch(batch_ids)

        final_dataset.extend(batch_data)

    return final_dataset
