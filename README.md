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

We had to add an error handler.  See below.

Google has suggested that the drive api call changes().list()
can be used to find all files a user owns.  This might be true.
See program sa-changes in the scripts directory.  Initial testing
has shown that this does work, but it can be much slower.
It depends a lot on what the shared history of the account is.

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

## Basic setup

The best place to find setup directions for a non-authorized setup
is [here](https://developers.google.com/drive/api/quickstart/python).

Basically:

- Create a Google Cloud project.
- Enable Google Drive API
- Enable the application
- Get credentials
- Put the credentials in a file called `credentials.json` in the directory you are running from. (Yuck.  Whatever. Send me a patch.)

## Installing

There is no installation procedure.  Run the code in the main
directory or supply a path to the scripts.

## Configuration

At this time, the path to a set of authorized credentials can be
used or you can follow the basic application setup steps above.
This document will not cover how to create credentials that allow
impersonation.  If you use GAM, for instance, those credentials
would work.  Set the path in the `sa_app/our_auth.py` module if you
want to use credentials that allow impersonation.  These would be
credentials similar to what you use to run **GAM**, for instance.

If you do not set such credentials, you must run the program
locally and will be prompted to authorize the application on your
web browser.

The default distribution assumes authorized credentials, so change
the path for `KEYS` to `''` in the `sa_app/our_auth.py` module.

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

A new program has been added called `sa-user` which uses

```
"<account-name@school.edu>" in owners
```

When I ran this on a sample account, it did return more files, but
by no means all.  However, I had submitted a ticket to Google by
this point and it is reasonable to assume that Google is reindexing
our accounts also.  I will add more information here as I get it.

to get a list of files based from My Drive.  Note that this will
include files owned by others if present.  So, you if you compare
the file ids from './sa', you will need to exclude those with
`"ownedByMe":true`.  `fgrep -v` or similar can do this.

> Specifying a user does nothing if you are using local authentication and is not required.  The code will run for whatever account you authorized via the web browser.

## Discussion

**sa-r** should return the same set of files that **sa** does,
if the files from sa are rooted at My Drive.  **sa** can return
files that are rooted elsewhere.  That is the whole point as to why
we would want to do a *"me" in owners* query in the first place.
We want to find computer backups which are not rooted from **My
Drive** and files in folders owned by other users that are not
on this user's path from **My Drive**.

## Total Space

We now report the total space found.  I also added the total
in MiB, TiB, etc because the admin console actually reports
in these units.  The reports that we can pull from the API use
units of 'mb', but are actually 'MiB', so keep that in mind when
comparing results from these programs to other data sources.
MiB is always printed to aid in comparing to the reports, no
matter how much space is used, along with the closest unit.

Additionally, I have switched from 'size' to 'quotaBytesUsed'.
It is hard to know what the admin console is reporting, but
generally I think this is a more useful number.

## Errors

### Non 500 Errors

As of now, I have not found any none-500 error codes generated by
this code, so I am not handling them.  I want this code to be as
simple and straight forward as possible.  Any production program
would of course handle at least 2 rate limit exceeded errors
and they can be 403s or 429s.  If you have a need to run many
copies of this code at the same time, or you are running other
programs that use the Drive API and are getting 403s or 429s,
we can add handling those codes as well.

### Error handler added.

```
Basic args: {'q': '"me" in owners', 'fields': 'nextPageToken,files(mimeType,id,name,trashed,explicitlyTrashed,parents,md5Checksum,sharingUser(permissionId,emailAddress,me),shared,createdTime,modifiedTime,modifiedByMeTime,trashingUser(emailAddress),trashedTime,size,shortcutDetails(*),webViewLink)', 'spaces': 'drive,appDataFolder', 'pageSize': 1000}
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/mike/src/Google-Drive-Simple/sa_app/sa.py", line 89, in <module>
  File "/home/mike/src/Google-Drive-Simple/sa_app/sa.py", line 71, in list
  File "/home/mike/src/Google-Drive-Simple/env/lib64/python3.11/site-packages/googleapiclient/_helpers.py", line 130, in positional_wrapper
  File "/home/mike/src/Google-Drive-Simple/env/lib64/python3.11/site-packages/googleapiclient/http.py", line 938, in execute
googleapiclient.errors.HttpError: <HttpError 500 when requesting https://www.googleapis.com/drive/v3/files?q=%22me%22+in+owners&fields=nextPageToken%2Cfiles%28mimeType%2Cid%2Cname%2Ctrashed%2CexplicitlyTrashed%2Cparents%2Cmd5Checksum%2CsharingUser%28permissionId%2CemailAddress%2Cme%29%2Cshared%2CcreatedTime%2CmodifiedTime%2CmodifiedByMeTime%2CtrashingUser%28emailAddress%29%2CtrashedTime%2Csize%2CshortcutDetails%28%2A%29%2CwebViewLink%29&spaces=drive%2CappDataFolder&pageSize=1000&pageToken=~%21%21~AI9FV7RutP00ibTMGkkacjK6ZSCaGvyGuo3-JYgOHnKfi5Sh8C1j_HFT1fVfIwHb5cBKi4r1hLzCIlVtqzELyB40e2-VfWgK1WtGH9m-bqlODDl8ZpuGJntNmN-1wNmxxpUV_sKwXmqpaM6pBjBV36kAQ0L253tI8yHO5lPAiyZTF4WuNWlnt7sahXY8CbOUK544MOly3O7LuNRZJmvYwyB_XBhBWY9mmcY7YiHCBYCzuI_8OteM12h7-DaaWiXqdnJ0-NUGjLstTNDKM0pRR8l4yqO90u5xjUxK0H_zAhT-kTveFZu_wGbqW0MTrNK7XiJ8DzPKeEyygoJD67v56JBkDYEwXEVRbg%3D%3D&alt=json returned "Internal Error". Details: "[{'message': 'Internal Error', 'domain': 'global', 'reason': 'internalError'}]">
```

And another

```
Basic args: {'fields': 'nextPageToken,files(mimeType,id,name,trashed,explicitlyTrashed,parents,owners(permissionId,emailAddress),ownedByMe,md5Checksum,sharingUser(permissionId,emailAddress,me),shared,createdTime,modifiedTime,modifiedByMeTime,trashingUser(emailAddress),trashedTime,size,shortcutDetails(*),webViewLink)', 'spaces': 'drive,appDataFolder', 'pageSize': 1000}
Traceback (most recent call last):
  File "/usr/lib64/python3.9/runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/lib64/python3.9/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/home/mike/src/Google-Drive-Simple/sa_app/sa_r.py", line 96, in <module>
    list()      # Run the program.
  File "/home/mike/src/Google-Drive-Simple/sa_app/sa_r.py", line 72, in list
    v = drive_service.files().list( **args ).execute()
  File "/home/mike/src/Google-Drive-Simple/env/lib64/python3.9/site-packages/googleapiclient/_helpers.py", line 130, in positional_wrapper
    return wrapped(*args, **kwargs)
  File "/home/mike/src/Google-Drive-Simple/env/lib64/python3.9/site-packages/googleapiclient/http.py", line 938, in execute
    raise HttpError(resp, content, uri=self.uri)
googleapiclient.errors.HttpError: <HttpError 500 when requesting https://www.googleapis.com/drive/v3/files returned "Internal Error". Details: "[{'message': 'Internal Error', 'domain': 'global', 'reason': 'internalError'}]">
```

Clearly we needed an error handler.  The Google APIs are not
robust enough.  If not restartable, then Google has an issue
since we can't audit what they are charging us for.
