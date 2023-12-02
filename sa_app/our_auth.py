"""
Routine to handle authentication.
"""

import sys
import pprint
import httplib2
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient import errors
import googleapiclient
import oauth2client

USER=sys.argv[ 1 ]
KEYS = '/usr/local/keys/ga-g-suite-administration-0357ee3510c2.json'

scopes = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.appdata',
    'https://www.googleapis.com/auth/drive.metadata',
    'https://www.googleapis.com/auth/drive.photos.readonly',
]

def our_connect():

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
