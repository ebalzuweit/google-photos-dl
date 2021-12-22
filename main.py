import configparser
import pickle
import os.path
import requests

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CONFIG_PATH = './config.ini'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def get_credentials(creds_file = 'credentials.json', token_file = 'token.pickle'):    
    creds = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def enumerate_photos(photos_api, album_id, download_path):
    photo_search_req = photos_api.search(body={'albumId': album_id})
    while photo_search_req is not None:
        photo_results = photo_search_req.execute()
        photos = photo_results['mediaItems']
        download_photos_from_mediaItems(photos, download_path)
        photo_search_req = photos_api.list_next(photo_search_req, photo_results)

def download_photos_from_mediaItems(photos, download_path):
    # https://developers.google.com/photos/library/guides/access-media-items#base-urls
    for photo in photos:
        filename = photo['filename']
        filepath = os.path.join(download_path, filename)
        baseUrl = photo['baseUrl']
        width = photo['mediaMetadata']['width']
        height = photo['mediaMetadata']['height']
        requestUrl = f'{baseUrl}=d-w{width}-h{height}'
        
        if not os.path.exists(filepath):
            img_data = requests.get(requestUrl).content
            with open(filepath, 'wb') as file:
                file.write(img_data)
                print(f'Downloaded {filename}')
        else:
            print(f'Skipping {filename}')

def main():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    creds = get_credentials()
    with build('photoslibrary', 'v1', credentials=creds, static_discovery=False) as service:
        enumerate_photos(service.mediaItems(), config.get('google-photos-dl', 'AlbumId'), config.get('google-photos-dl', 'DownloadFolder'))

if __name__ == '__main__':
    main()
