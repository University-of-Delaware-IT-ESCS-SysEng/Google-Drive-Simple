"""
Simple program that does a Google Drive API drive.list() call
using the query "me" in owners.  This should return all files a
user owns.  Does it?  Let's see.
"""

import sys
import pprint
from sa_app.our_auth import our_connect
from sa_app.util import iB
import json
from googleapiclient import errors
import googleapiclient
import sa_app.error

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
        ',quotaBytesUsed'
        ',shortcutDetails(*)'
        ',webViewLink' )

    ( user, drive_service ) = our_connect()

    args = {}
    args[ 'q' ] = '"%s" in owners' % user
    args[ 'fields' ] = 'nextPageToken,files(' + fields + ')'
    args[ 'spaces' ] = 'drive,appDataFolder'
    args[ 'pageSize' ] = 1000

    print( "INFO: Basic args: %s" % args, file=sys.stderr )

    total_size = 0

    while True:
        while True:
            try:
                v = drive_service.files().list( **args ).execute()
                break               # API call worked-ish
            except googleapiclient.errors.HttpError as e:
                r = sa_app.error.error_handler( e )
                if not r:
                    raise           # Program exit
                else:
                    print( "ERROR: Retrying args %s" % args, file=sys.stderr )
                    pass            # Will redo the same call with same args

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
                total_size += int( f[ 'quotaBytesUsed' ] )
            except ( KeyError, ValueError ):
                pass

        try:
            args[ 'pageToken' ] = v[ 'nextPageToken' ]
        except KeyError:
            break

    print( "INFO: quota bytes used found: %s %d (%s) (%s)" %
        ( user, total_size, iB( total_size ), iB( total_size, force_mib=True )),
        file=sys.stderr )

list()

# End.
