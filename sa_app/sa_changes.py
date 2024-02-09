"""
Simple program that does a Google Drive API changes.list() call.
A claim has been made by Google that this will return all files
owned by a user.  An initial test on a known large account that
never lists all the files for a standard "me" in owners did in
fact find all files.  Doing some more testing.
"""

import sys
import pprint
from sa_app.our_auth import our_connect
from sa_app.util import iB
import json
from googleapiclient import errors
import googleapiclient
import sa_app.error

#
# Defining this flag to be True will generate JSON that works
# with University of Delaware internal tools.
#

UOFD=True

def list():

    fields = ( 'mimeType,id,name,trashed,explicitlyTrashed'
        ',parents'
        ',md5Checksum'
        ',shared'
        ',createdTime'
        ',modifiedTime'
        ',modifiedByMeTime'
        ',trashingUser(emailAddress)'
        ',trashedTime'
        ',ownedByMe'
        ',quotaBytesUsed'
        ',shortcutDetails(*)'
        ',webViewLink' )

    ( user, drive_service ) = our_connect()

#
# If you want all changes, start with page 1.
#

    startPageToken = 1

    args = {}
    args[ 'includeCorpusRemovals' ] = 'true'
    args[ 'includeRemoved' ] = 'false'
    args[ 'includeItemsFromAllDrives' ] = 'false'
    args[ 'supportsAllDrives' ] = 'true'
    args[ 'fields' ] = ( 'nextPageToken,newStartPageToken,changes(file('
                            + fields + '))' )
    args[ 'spaces' ] = 'drive'
    args[ 'pageSize' ] = 1000
    args[ 'pageToken' ] = startPageToken

    print( "INFO: Basic args: %s" % args, file=sys.stderr )

    if UOFD:
        print( '{ "%s": { "drive-ls": {' % user )
        first=True

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

        for c in v[ 'changes' ]:

            # Makes working with Unix text tools easy

            f = c[ 'file' ]
            try:                    # Skip files not owned by this user
                if not f[ 'ownedByMe' ]:
                    continue
                del f['ownedByMe']  # Save space
            except KeyError:
                continue            # ownedByMe: false does not appear.

            if UOFD:
                if not first:
                    print( ",", end='' )
                else:
                    first = False

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

    if UOFD:
        print( "}}}" )

    print( "INFO: quota bytes used found: %s %d (%s) (%s)" %
        ( user, total_size, iB( total_size ), iB( total_size, force_mib=True )),
        file=sys.stderr )

list()

# End.
