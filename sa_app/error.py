"""
The sadly required error handling module.  There just isn't a
way to get 10,000,000 files from a drive.files.list call without
getting at least one internal error.
"""

import sys
import json
import time

def error_handler( e ):

    """
    This is the error handler.  It takes an exception and tries to
    determine if we can retry.

    This routine should called from an exception handler.

    Arguments:

        e: Currently an error from class oogleapiclient.errors.HttpError,
            but we may have to expand on this.

    Returns:
        True: We can retry the call with the same arguments.
        False: We should raise the error again.
    """

    try:
        error = json.loads( e.context )
    except ValueError:              # Error that is not JSON.
        return( False )

    try:
        code = error[ 'error' ][ 'code' ]
    except KeyError:
        code = '<none>'

    try:
        first_error = error[ 'error' ][ 'errors' ][ 0 ]
    except KeyError:
        first_error = error[ 'error' ]      # Just one error

    try:
        reason = first_error[ 'reason' ]
    except KeyError:
        reason = ''

#
# Fancier backoffs are used in production code.  This is code made to be
# simple.  A 5 second backoff on an internal error is more than fine.
#

    if code == 500 and reason == 'internalError':
        print( "ERROR: %s" % e, file=sys.stderr )
        print( "ERROR: Retrying error after sleeping 5 seconds.",
            file=sys.stderr )
        time.sleep( 5 )
        return( True )
    else:
        return( False )

#
# End.
