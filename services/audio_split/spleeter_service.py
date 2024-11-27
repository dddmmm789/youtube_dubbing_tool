# spleeter_service.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import time

class SpleeterService:
    def __init__(self):
        self.service = self._build_drive_service()
        self.input_folder_id = '1-7HnIyuqm8eA5oc47A-0FW_i66Igsy-E'  # Your Drive folder IDs
        self.output_folder_id = '1-5Eg7BqqEWWZyfzjBHyTciMVWT7mjfrx'

    def process_audio(self, file_path):
        """Process audio file through Colab Spleeter service"""
        try:
            # 1. Upload to Drive input folder
            print(f"Uploading: {file_path}")
            self._upload_file(file_path)
            
            # 2. Wait for processing
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = f"{base_name}/vocals.wav"  # Spleeter's output structure
            
            print("Waiting for processing...")
            while not self._check_output(output_path):
                time.sleep(5)
            
            print("Processing complete!")
            return True
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def _build_drive_service(self):
        """Build Google Drive service"""
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        return build('drive', 'v3', credentials=creds)

    def _upload_file(self, file_path):
        """Upload file to Drive input folder"""
        file_name = os.path.basename(file_path)
        file_metadata = {
            'name': file_name,
            'parents': [self.input_folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

    def _check_output(self, output_path):
        """Check if output file exists"""
        results = self.service.files().list(
            q=f"'{self.output_folder_id}' in parents",
            fields="files(name)"
        ).execute()
        files = results.get('files', [])
        return any(output_path in f['name'] for f in files)