import os
from dotenv import load_dotenv
import requests as req
import json
from datetime import datetime
import pandas as pd

load_dotenv()
base_url = os.getenv("BASE_URL")

def get_api_key():
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("API Key not found. Please check your .env file.")
    return api_key

def get_channel_id(handle):
    params = {
    "part": "id",
    "forHandle": handle
    }
    res = req.get(f"{base_url}/channels",params=params | {"key": get_api_key()}).json()

    return res['items'][0]['id']


def download_banner(handle,file_name,folder_path):
    params = {
        "part": "brandingSettings",
        "forHandle": handle
    }
    banner_url = req.get(f"{base_url}/channels", params=params | {"key": get_api_key()}).json()["items"][0]["brandingSettings"]["image"][
        "bannerExternalUrl"]
    path = os.path.join(folder_path, file_name)

    try:
        # 3. Stream the request (efficient for large files/banners)
        response = req.get(banner_url, stream=True)
        response.raise_for_status()  # Check for errors (404, 500, etc.)

        # 4. Save the binary data
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Image saved successfully: {path}")
    except Exception as e:
        print(f"❌ Failed to save image: {e}")



def save_data_to_json(data, filepath):
    # 1. Extraire le chemin du dossier depuis le filepath complet
    directory = os.path.dirname(filepath)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as file:

        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"✅ Données sauvegardées avec succès dans : {filepath}")



def etl_channel_statistics(handle, save_folder_path="./data/processed/"):
    # Ensure folder exists
    os.makedirs(save_folder_path, exist_ok=True)

    output_path = os.path.join(save_folder_path, "channel_stats.csv")

    # -------- EXTRACT --------
    channel_id = get_channel_id(handle)

    params = {
        "part": "snippet,statistics",
        "id": channel_id
    }

    res = req.get(f"{base_url}/channels", params=params | {"key": get_api_key()}).json()
    items = res.get("items", [])

    if not items:
        print("No channel data found.")
        return

    item = items[0]

    # -------- TRANSFORM --------
    snippet = item.get("snippet", {})
    statistics = item.get("statistics", {})

    channel_data = {
        "channelId": item.get("id"),
        "channelTitle": snippet.get("title"),
        "publishedAt": snippet.get("publishedAt"),
        "subscriberCount": int(statistics.get("subscriberCount", 0)) if statistics.get("subscriberCount") else None,
        "viewCount": int(statistics.get("viewCount", 0)) if statistics.get("viewCount") else None,
        "videoCount": int(statistics.get("videoCount", 0)) if statistics.get("videoCount") else None,
        "extractedAt": datetime.utcnow().isoformat()
    }

    df = pd.DataFrame([channel_data])

    # -------- LOAD (overwrite) --------
    df.to_csv(output_path, index=False)

    print(f"Channel statistics overwritten at {output_path}")