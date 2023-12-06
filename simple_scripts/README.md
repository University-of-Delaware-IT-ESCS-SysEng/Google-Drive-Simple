# Simple queue scripts.

Some simple scripts to make running a constrained number of
scripts at once easier.  We find we can run 75 processes doing
drive.files().list and use about 20% of our quota. Our quota has
not been increased by Google.

## Using run.sh

This script will run a lot of copies of the script doit.sh.

Make the following:

```
mkdir gd-run
mkdir gd-run/in
mkdir gd-run/logs
mkdir gd-run/out
mkdir gd-run/running
mkdir gd-reports
```

Edit doit.sh to set your domain any any paths you need to adjust.

Touch files in gd-run as so:

```
touch gd-run/in/mike
```

Use a for loop or something to save time.

Then run

```
./run.sh
```

To find the missing file ids, I usually do something like:

```
for i in `ls gd-reports`; do
    ./find_missing.sh ${i}
done
```

This script runs pretty fast and uses a lot of CPU and memory,
so I typically run it synchronously.  This is why it is not part
of doit.sh.  You would not want to accidentally run 75 copies of
the find_missing script at the same time.

End.
