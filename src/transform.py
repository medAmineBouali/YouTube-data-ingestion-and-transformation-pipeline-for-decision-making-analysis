import pandas as pd
from datetime import datetime

def transform_and_save(raw_data_file_path,save_folder_path = "./"):
    print("loading raw data...")
    df = pd.read_json(raw_data_file_path)

    print("Transforming data...")
    # 2. Clean the topic URLs to extract just the category name (e.g., "Entertainment")
    df["topicCategories"] = df["topicCategories"].apply(lambda x: [topic.replace("https://en.wikipedia.org/wiki/", "") for topic in x])

    # 3. Create the Bridge Table using explode

    topic_df = df[["videoId","topicCategories"]].explode("topicCategories").dropna(subset=["topicCategories"]).rename(columns={'topicCategories': 'topic'})

    df = df.drop(columns=["topicCategories"])

    # 5. processing the time columns
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['publish_date'] = df['publishedAt'].dt.date
    df['publish_hour'] = df['publishedAt'].dt.hour
    df['publish_time'] = df['publishedAt'].dt.time

    df['duration'] = pd.to_timedelta(df['duration'])

    # keep numeric version for Power BI
    df['duration_seconds'] = df['duration'].dt.total_seconds().astype(int)

    # convert display column before export
    df['duration'] = df['duration'].astype(str).str.replace('0 days ', '', regex=False)

    #6. saving the dataframes
    print("saving to csv...")
    df.to_csv(f"{save_folder_path}videos.csv", index=False)
    topic_df.to_csv(f"{save_folder_path}topics.csv", index=False)


    #timestamp = datetime.now().strftime("%Y-%m-%d")
    #df.to_csv(f"{save_folder_path}videos_{timestamp}.csv", index=False)
    #topic_df.to_csv(f"{save_folder_path}topics_{timestamp}.csv", index=False)
