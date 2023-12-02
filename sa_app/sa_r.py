"""
Future program that will do a recursive list of
the user's My Drive.
"""

import sys
import pprint
import json

from collections import deque

from googleapiclient import errors
import googleapiclient

from sa_app.our_auth import our_connect

_FOLDER_MT = 'application/vnd.google-apps.folder'

def list():

    fields = ( 'mimeType,id,name,trashed,explicitlyTrashed'
        ',parents'
        ',owners(permissionId,emailAddress)'
        ',ownedByMe'
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

    drive_service = our_connect()

    args = {}
    args[ 'fields' ] = 'nextPageToken,files(' + fields + ')'
    args[ 'spaces' ] = 'drive,appDataFolder'
    args[ 'pageSize' ] = 1000

    print( "Basic args: %s" % args, file=sys.stderr )

    dirs = deque()
    dirs.append( 'root' )

#
# Build something like ('id1' in parents or 'id2' in parents) maxed at 50.
# this does slightly complicate the program, but the speed up is truly
# dramatic and the code isn't all that complicated.
#

    while dirs:
        MAX_PARENTS = 50

        parents = '('
        for i in range( min( len( dirs ), MAX_PARENTS ) ):
            dir = dirs.popleft()
            parents += f"'{dir}' in parents or "
        parents = parents[0:-4]         # Get rid of trailing " or "
        parents += ')'                  # Close query

        args[ 'q' ] = parents
        try:                            # Could be left over from prior list
            del args[ 'pageToken' ]
        except KeyError:
            pass

        while True:
            v = drive_service.files().list( **args ).execute()
            for f in v[ 'files' ]:
                if f[ 'mimeType' ] == _FOLDER_MT:
                    dirs.append( f[ 'id' ] )

                # Makes working with Unix text tools easy

                print( '"%s":' % f[ 'id' ], end='' )
                json.dump( f, sys.stdout,
                            sort_keys=False,
                            check_circular=False,
                            indent=None,
                            separators=(',', ':') )
                print( '' )                     # One line per file

            # End of files for loop

            try:
                args[ 'pageToken' ] = v[ 'nextPageToken' ]
            except KeyError:
                break
        # End of paging loop for a files().list call series on set of parents
    # End of loop that processes all located directories

list()      # Run the program.

# End.
