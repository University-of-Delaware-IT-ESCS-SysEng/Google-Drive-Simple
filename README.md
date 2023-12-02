# Google-Drive-Simple Application.

Serious consideration is being given to the problem that some of us
have seen in that:

> The Google Drive API does not return all files when a *"me" in owners*
query is performed.

The programs in this repository attempt to prove this by presenting a simple
program that lists all files found by the *"me" in owners* query, and
a program that recursively processes all files located from a user's
*My Drive* and lists them in a similar way.

We anticipate using simple unix text processing tools to process the
resulting lists of files and show that files are missing on at least
some accounts for *"me" in owners* query.

Initial observations seem to indicate that the same files are always missing
when the query is done.  However, I have recently noted a large account
that has far more missing files now than it ever did in the past.  This
may suggest a deteriorating situation.  However, this has not been proved
yet.

The code is somewhat problematic because it can be difficult to
get a large file list from a big account without error handling.
However, I have removed all error handling because Google won't
be able to claim the non-existent error handling is incorrect.
Time will tell if error handling will be required and Google
will either need to provide guidance on what the proper error
handling is, or if indeed error handling can even be used in a
multipage listing.  Maybe large lists of files are just broken.
Who knows what Google will say.

## Downloading

Download like you would any git repository.

## Setting up the Environment

In the Makefile, set your python executable name.

This application uses a Python environment that is dynamically built.
So long as you have a Python3 installation, this code should work.
If you come across a missing module situation, please submit a patch
againsts the releases.txt file.

Setup:

```
make env
make bin
```

If you change the location of the program, you may need to redo the
`make bin` step.

## Security

The following scopes are used:

```
https://www.googleapis.com/auth/drive.readonly
https://www.googleapis.com/auth/drive.metadata.readonly
https://www.googleapis.com/auth/drive.appdata
```
There is no readonly version of *drive.appdata* that I know of.

## Installing

There is no installation procedure.  Run the code in the main
directory or supply a path to the scripts.

## Configuration

At this time, the path to a set of authorized credentials is required.
Set the path in the `sa_app/our_auth.py` module.  These would be
credentials similar to what you use to run **GAM**, for instance.

Later on today, most likely, I will add code that allows for
local authentication so that those of you who do not want to
supply privileged keys will not need to.  Of course, you will
then need to be able to login to the accounts under test.

## Running the programs

Run

```
./sa theuser@yourschool.edu > my.json
```

to get the list of files using the *"me" in owners* type query.

Run

```
./sa-r theuser@yourschool.edu > my-r.json
```

to get a list of files based from My Drive.  Note that this will
include files owned by others if present.  So, you if you compare
the file ids from './sa', you will need to exclude those with
`"ownedByMe":true`.  `fgrep -v` or similar can do this.

## Discussion

**sa-r** should return the same set of files that **sa** does,
if the files from sa are rooted at My Drive.  **sa** can return
files that are rooted elsewhere.  That is the whole point as to why
we would want to do a *"me" in owners* query in the first place.
We want to find computer backups which are not rooted from **My
Drive** and files in folders owned by other users that are not
on this user's path from **My Drive**.
