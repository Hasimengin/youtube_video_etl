import requests
import  json
import os
import dotenv
from datetime import datetime
dotenv.load_dotenv()    


API_KEY=os.getenv("API_KEY")
CHANELL_HANDLE="MrBeast"

def get_playListId():
    try:
        url=f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANELL_HANDLE}&key={API_KEY}' 
        response=requests.get(url)
        response.raise_for_status()
        data=response.json() 
        chanell_items=data["items"][0]
        chanell_playListId=chanell_items["contentDetails"]["relatedPlaylists"]["uploads"]
        return chanell_playListId
    except requests.exceptionsRequestException as e:
        raise e



def get_video_ids(playlistId):
    maxResults=50
    base_url=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"
    try:
        video_ids=[]
        page_token=""
        while True:
            url=base_url
            if page_token:
                url+=f"&pageToken={page_token}"
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            items=data.get("items",[])
            for item in items:
                video_id=item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            page_token=data.get("nextPageToken")
            if not page_token:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e                 

def batch_video_ids(video_ids, batch_size=50):
    for i in range(0, len(video_ids), batch_size):
        yield video_ids[i:i + batch_size]

def extract_video_data(video_ids):
    all_video_stats=[]
    try:
        for batch in batch_video_ids(video_ids):
            ids=",".join(batch)
            url=f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={ids}&key={API_KEY}'
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            items=data.get("items",[])
            for item in items:
                video_stat={
                    "video_id":item["id"],
                    "title":item["snippet"]["title"],
                    "publishedAt":item["snippet"]["publishedAt"],
                    "viewCount":item["statistics"].get("viewCount","0"),
                    "likeCount":item["statistics"].get("likeCount","0"),
                    "commentCount":item["statistics"].get("commentCount","0"),
                }
                all_video_stats.append(video_stat)
        return all_video_stats
    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(data):
    file_path=f"./data/YT_data_{datetime.today()}.json"
    with open(file_path , "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)    


if __name__ == "__main__":
    playlistId=get_playListId()
    video_ids=get_video_ids(playlistId)
    all_video_stats=extract_video_data(video_ids)
    save_to_json(all_video_stats)