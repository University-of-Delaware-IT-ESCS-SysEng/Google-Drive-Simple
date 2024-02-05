"""
Simple program that does a Google Drive API changes.list() call.
A claim has been made that this will return all files owned by
a user.  Or at least a lot of them.  Currently, this program
never returns any changes.  I don't know why.
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

#
# We'll just let this call run without error handling.
# Most likely if it fails we want to abort the entire
# run anyhow.
#

    args = {}
    v = drive_service.changes().getStartPageToken().execute()
    startPageToken = v[ 'startPageToken' ]

    print( 'INFO: getStartPageToken returned %s' % startPageToken )

    args = {}
#    args[ 'includeCorpusRemovals' ] = 'true'
#    args[ 'includeRemoved' ] = 'false'
    args[ 'fields' ] = 'nextPageToken,newStartPageToken,changes(file(' + fields + '))'
    args[ 'spaces' ] = 'drive'
#    args[ 'pageSize' ] = 1000
    args[ 'pageToken' ] = startPageToken

    print( "INFO: Basic args: %s" % args, file=sys.stderr )

    total_size = 0

    while True:
        while True:
            try:
                v = drive_service.changes().list( **args ).execute()
                break               # API call worked-ish
            except googleapiclient.errors.HttpError as e:
                r = sa_app.error.error_handler( e )
                if not r:
                    raise           # Program exit
                else:
                    print( "ERROR: Retrying args %s" % args, file=sys.stderr )
                    pass            # Will redo the same call with same args

        pprint.pprint( v )
        for c in v[ 'changes' ]:

            # Makes working with Unix text tools easy

            f = c[ 'file' ]
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
