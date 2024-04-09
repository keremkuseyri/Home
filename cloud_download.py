from googleapiclient.http import MediaIoBaseDownload
import io
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os 

CLIENT_SECRET_FILE = 'reportapi-419616-d09ede636e47.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

def download_folder(service, folder_id, local_folder_path):
    query = f"'{folder_id}' in parents and trashed=false"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])

    if not files:
        print('No files found in the folder.')
        return

    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)
    
    for file in files:
        file_id = file.get('id')
        file_name = file.get('name')
        file_path = os.path.join(local_folder_path, file_name)

        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()

        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        with open(file_path, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
            print(f'Downloaded {file_name} to {file_path}')

def authenticate():
    creds = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)
    return build(API_NAME, API_VERSION, credentials=creds)


if __name__ == "__main__":
    service = authenticate()

    parent_folder_ids = {
        "sea_raw_data": "1guOcc2mxPNGP7Y_u9zJr4fNFyCbquQg5", 
        "sea_forecasting": "1tjHHLsHV7QDa563TVE4rEUkbFbvpg-cp",
        "air_raw_data": "1BGM0-mf1jJV139QrYlR-HOopxKGWT4Co",
        "air_forecasting": "1nFYRjNpORJvlHK-xVkcH9PzfrCW3GBBE",
        "air_import_employee_kpis": "1tUY_12zC2CQALC02vhcyAqaaX-HPHykr",
        "air_export_employee_kpis": "13pvxWaGvEp-k2E3-bAuBsEKXqfksgVVr"
    }

    for folder_name, parent_folder_id in parent_folder_ids.items():
        download_folder(service, parent_folder_id, os.path.join(os.getcwd(), "reports/" + folder_name))

