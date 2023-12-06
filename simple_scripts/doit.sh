#!/bin/bash
#
# This script is designed to be run from run.sh
#
# Args:
#   user
#   source-queue-file
#   destination folder to move source-queue-file to when done.

GDUSER=${1}
echo Starting ${GDUSER}

#
# This can generate a lot of output
# if you run it for lots of people.
# Perhaps a symlink to a file system
# with lots of storage?
#

DOMAIN="@udel.edu"
BASE="."
SCRIPTS="."
SA_SCRIPTS=".."

# You will likely want to symlink this elsewhere.
# ie: ln -s /data/mike/gd-reports-2023-12-04 gd-reports

GDREPORTS=${SCRIPTS}/gd-reports

mkdir -p ${GDREPORTS}/${GDUSER}

${SA_SCRIPTS}/sa ${GDUSER}${DOMAIN} > ${GDREPORTS}/${GDUSER}/${GDUSER}.json
RC=$?
if [ ${RC} -gt 0 ]; then
    echo mv ${2} ${3}/${1}.err
    mv ${2} ${3}/${1}.err
    exit 0
fi

${SA_SCRIPTS}/sa-r ${GDUSER}${DOMAIN} > ${GDREPORTS}/${GDUSER}/${GDUSER}-r.json
RC=$?
if [ ${RC} -gt 0 ]; then
    echo mv ${2} ${3}/${1}.err
    mv ${2} ${3}/${1}.err
else
    echo mv ${2} ${3}
    mv ${2} ${3}
fi

#
# End.
