"""
General utility routines.
"""

KiB = 1024
MiB = KiB * KiB
GiB = MiB * KiB
TiB = GiB * KiB
PiB = TiB * KiB

def iB( v, decimal_places=2, force_mib=False ):

    """
    Prints an input integer in the closest standard unit (i, KiB, MiB,
    TiB, PiB) and puts the unit type used.  Two decimal places is the
    default.
    """

    if force_mib:
        ( d, u ) = ( MiB, "MiB" )
    else:
        for d, u in ( ( PiB, "PiB" ), ( TiB, "TiB" ), ( GiB, "GiB" ),
                ( MiB, "MiB" ), ( KiB, "KiB" ) ):
            if v >= d:
                break
        else:
            d = 1
            u = None

    if u:
        return( "{0:.0{decimal_places}f} {1:s}".format(
                v/d, u, decimal_places=decimal_places ) )
    else:
        return( "%d" % v )

##
# End of iB.
##

if __name__ == '__main__':
    print( iB( 1000 ) )
    print( iB( 2000 ) )
    print( iB( PiB ) )
    print( iB( 12345678944555, force_mib = True ) )
