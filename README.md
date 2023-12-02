# Google-Drive-Simple
Simple Google Drive API code.

In Makefile, set your python executable name.

Run:

make env

make bin

Run ./sa theuser@yourschool.edu > my.json  to get the list of files.

Run ./sa-r theuser@yourschool.edu > my-r.json to get a list of
files based from My Drive.  note that this will include files owned
by others if present.  So, you if you compare the file ids from
'./sa', you will need to exclude those with ownedbyMe: false.
