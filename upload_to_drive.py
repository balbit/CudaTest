import os
import argparse
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import json


def get_default(field):
    with open('utils/defaults.json', 'r') as file:
        defaults = json.load(file)
        return defaults.get(field)


def get_credentials_path():
    credentials_path = get_default('drive_key_path')

    while not os.path.exists(credentials_path) or os.path.getsize(credentials_path) == 0:
        credentials_path = input("Enter the path to your service account credentials JSON file: ")
    return credentials_path


def get_existing_file_id(drive_service, folder_id, file_name):
    response = drive_service.files().list(q=f"'{folder_id}' in parents and name = '{file_name}' and trashed = false",
                                          spaces='drive',
                                          fields='files(id)').execute()
    files = response.get('files', [])
    return files[0]['id'] if files else None


def upload_file(credentials_file, folder_id, local_file_path, overwrite=False):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    file_name = os.path.basename(local_file_path)
    file_metadata = {'name': file_name}

    existing_file_id = get_existing_file_id(drive_service, folder_id, file_name)

    media = MediaFileUpload(local_file_path)

    if existing_file_id:
        if not overwrite:
            overwrite_file = input(f'File "{file_name}" already exists. Do you want to overwrite it? (y/n): ')
            if overwrite_file.lower() != 'y':
                print('File upload cancelled.')
                return
        updated_file = drive_service.files().update(fileId=existing_file_id, body=file_metadata, media_body=media).execute()
        print(f'Updated existing file "{file_name}" with ID: {updated_file.get("id")}')
    else:
        file_metadata['parents'] = [folder_id]
        created_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'Created new file "{file_name}" with ID: {created_file.get("id")}')


def main():
    parser = argparse.ArgumentParser(description='Upload a file to Google Drive.')
    parser.add_argument('file_path', help='Path to the file to be uploaded')
    parser.add_argument('--credentials', default=f'{get_credentials_path()}', help='Path to Google service account credentials')
    parser.add_argument('--folder_id', default=f'{get_default("folder")}', help='ID of the Google Drive folder to upload the file to. Note that this is not a filepath, but can be acquired from the URL of the folder.')
    parser.add_argument('--overwrite', default=False, help='Default to False. If True, will overwrite existing files with the same name.')
    
    args = parser.parse_args()

    upload_file(args.credentials, args.folder_id, args.file_path)

if __name__ == '__main__':
    main()
