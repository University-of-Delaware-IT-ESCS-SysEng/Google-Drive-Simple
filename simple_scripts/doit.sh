#!/bin/bash
#
# Args:
#   user
#   source-queue-file
#   destination folder to move source-queue-file to when done.

echo Starting ${1}

#/home/mike/bin/gd-json-only.sh ${1}
/home/mike/bin/gd-json-ls-d-only.sh ${1}
if [ $? -gt 0 ]; then
    echo mv ${2} ${3}/${1}.err
    mv ${2} ${3}/${1}.err
else
    echo mv ${2} ${3}
    mv ${2} ${3}
fi
