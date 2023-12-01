from __future__ import print_function

"""
Figure out sharingUser and how it can be used.

The drive API.
"""

import sys
import pprint
import httplib2
import oauth2client
import json
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient import errors
import googleapiclient
import oauth2client

USER='mike@udel.edu'
keys = '/usr/local/keys/ga-g-suite-administration-0357ee3510c2.json'

scopes = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.appdata',
    'https://www.googleapis.com/auth/drive.metadata',
    'https://www.googleapis.com/auth/drive.photos.readonly',
]

def connect():

    undelegated_credentials = (
        ServiceAccountCredentials.from_json_keyfile_name(
        keys, scopes=scopes ) )
    o2_credentials = undelegated_credentials.create_delegated( USER )
    http = httplib2.Http()
    o2_credentials.authorize( http )
    drive_service = build( 'drive', 'v3', http=http )

    return( drive_service )

def list():

    fields = ( 'mimeType,id,name,trashed,explicitlyTrashed'
        ',parents'
        ',md5Checksum'
        ',sharingUser(permissionId,emailAddress,me)'
        ',shared'
        ',createdTime'
        ',modifiedTime'
        ',modifiedByMeTime'
        ',trashingUser(emailAddress)'
        ',trashedTime'
        ',size'
        ',shortcutDetails(*)'
        ',webViewLink' )

    drive_service = connect()

    args = {}
    args[ 'q' ] = '"me" in owners'
    args[ 'fields' ] = 'nextPageToken,files(' + fields + ')'
    args[ 'spaces' ] = 'drive,appDataFolder'

    print( "Basic args: %s" % args, file=sys.stderr )

    while True:
        v = drive_service.files().list( **args ).execute()
        for f in v[ 'files' ]:

            # Makes working with Unix text tools easy

            print( '"%s":' % f[ 'id' ], end='' )
            json.dump( f, sys.stdout,
                        sort_keys=False,
                        check_circular=False,
                        indent=None,
                        separators=(',', ':') )
            print( '' )                     # One line per file

        try:
            args[ 'pageToken' ] = v[ 'nextPageToken' ]
        except KeyError:
            break

list()

# End.
