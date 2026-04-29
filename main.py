import os
from dotenv import load_dotenv

from src.extract import (
    get_playlist_id,
    get_all_video_ids,
    get_all_videos_dataset,
    save_data_to_json
)
from src.transform import transform_and_save


def main():
    # Charger les variables d’environnement
    load_dotenv()
    channel_handle = os.getenv("CHANNEL_HANDLE")

    if not channel_handle:
        raise ValueError("CHANNEL_HANDLE manquant dans le fichier .env")

    print(f"\n1. Fetching channel id for {channel_handle}")
    # Récupérer l’ID de la playlist "Uploads"
    playlist_id = get_playlist_id(channel_handle)
    print(f"\n2. Fetching all video ids ... ")
    # Récupérer tous les IDs des vidéos
    all_videos_ids = get_all_video_ids(playlist_id)
    print(f"\n3. Fetching data for all the videos by batching ... ")

    # Extraire les données des vidéos (batching)
    final_dataset = get_all_videos_dataset(all_videos_ids)

    raw_data_path = "data/raw/youtube_raw_data.json"
    print(f"\n4. Saving to {raw_data_path} ")

    # Sauvegarder les données brutes en JSON
    save_data_to_json(final_dataset, raw_data_path)

    transform_and_save(raw_data_file_path='./data/raw/youtube_raw_data.json',save_folder_path="./data/processed/")

if __name__ == "__main__":
    main()