"""
Routine to handle authentication.
"""

import sys
import pprint
import httplib2
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
import googleapiclient
import oauth2client

USER=sys.argv[ 1 ]
KEYS = '/usr/local/keys/ga-g-suite-administration-0357ee3510c2.json'
#KEYS = ''

scopes = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
# There is no readonly version of this scope that I know of
    'https://www.googleapis.com/auth/drive.appdata'
]

def our_connect():

    if not KEYS:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", scopes )
        o2_credentials = flow.run_local_server( port = 0 )
        drive_service = build( 'drive', 'v3', credentials=o2_credentials )
    else:
        undelegated_credentials = (
            ServiceAccountCredentials.from_json_keyfile_name(
            KEYS, scopes=scopes ) )
        o2_credentials = undelegated_credentials.create_delegated( USER )

        http = httplib2.Http()
        o2_credentials.authorize( http )
        drive_service = build( 'drive', 'v3', http=http )

        print( "Connected with user %s" % USER, file=sys.stderr )

    return( drive_service )

# End.
