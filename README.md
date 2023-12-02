# Google-Drive-Simple
Simple Google Drive API code.

In Makefile, set your python executable name.

Run:

make env

make bin

Run ./sa theuser@yourschool.edu > my.json  to get the list of files.

Run ./sa-r theuser@yourschool.edu > my-r.json to get a list of
files based from My Drive.  Note that this will include files owned
by others if present.  So, you if you compare the file ids from
'./sa', you will need to exclude those with ownedbyMe: false.

sa-r should return the same set of files that sa does, if the
files from sa are rooted at My Drive.  sa can return files
that are rooted elsewhere.  That is the whole point as to ehy
we would want to do a "me" in owners query in the first place.
To find computer backups which are not rooted from My Drive and
files in folders owned by other users that are not on this user's
path from My Drive.
