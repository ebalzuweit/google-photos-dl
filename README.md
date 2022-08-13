# Google Photos DL

Download new images from a Google Photos album.

## Usage

1. Create a Google Cloud Project.
2. Create a credentials.json for your client. [Read more](https://cloud.google.com/docs/authentication).

    `cp ~/Downloads/client_secret_####.json ./credentials.json`
3. Create a config.ini file and update the AlbumId to the Album ID of your Google Photos Album. [Read more](https://developers.google.com/photos/library/reference/rest/v1/albums/list).

    `cp config-example.ini config.ini && vi config.ini`
4. Run the application. The first time you launch the application you will have to authenticate and give permissions, this creates a `token.pickle` file for future runs.

    `python main.py`