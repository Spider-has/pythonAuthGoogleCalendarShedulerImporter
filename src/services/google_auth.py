import os
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config.config import AUTH_MODE, CLIENT_SECRET_FILE, SERVICE_ACCOUNT_FILE, TOKEN_FILE

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleAuth:
    @staticmethod
    def get_credentials(auth_mode):
        if auth_mode == 'by-service':
            if not os.path.exists(SERVICE_ACCOUNT_FILE):
                raise FileNotFoundError(f"Service account file not found: {SERVICE_ACCOUNT_FILE}")
            return service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
        
        elif auth_mode == 'by-auth':
            creds = None
            if os.path.exists(TOKEN_FILE):
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                    creds = flow.run_local_server(port=0)
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            return creds
        
        else:
            raise ValueError(f"Unknown AUTH_MODE: {AUTH_MODE}")