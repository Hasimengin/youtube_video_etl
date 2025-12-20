import requests
import  json
import os
import dotenv
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
    
if __name__ == "__main__":
    get_playListId    ()
