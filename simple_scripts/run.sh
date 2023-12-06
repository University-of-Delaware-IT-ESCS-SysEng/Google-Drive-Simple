#!/bin/bash

#
# Simple script to run multiple copies of
# script, limited to some number.  Create
# the needed directories, put a command in
# doit.sh and start.  Ideally under tmux
# or screen.  The number of active commands
# tends to also report the fgrep, but meh.
# Simple but it works.  And it restarts.
# Best run on a system you have control over.
#
# Modify script 'doit.sh' to control what
# actually runs.
#

CMD='./doit.sh'
IN='./gd-run/in'
OUT='./gd-run/out'
RUNNING='./gd-run/running'
LOGS='./gd-run/logs'

#
# We find that wee can easily run 75 concurrent
# scripts, however, I am going to default to 2
# so I don't make a mess on someone's system
# if they run this without checking things out.
# Besides, testing with 2 is a good start to make
# sure paths and file systems are correct and
# up to the task.  Note that there is bug
# that counts the fgrep as a process, so really
# set this to three to run two.
#

MAX=3
echo Running ${MAX} scripts in parallel.

mkdir -p ${IN}

while true; do
    active=`ps auxww | fgrep "${CMD}" | wc -l`

    if [ ${active} -lt ${MAX} ]; then
        NEXT=`ls ${IN} | head -1`
        if [ "x${NEXT}" = "x" ]; then
            echo Finished input queue
            break
        fi
        mv ${IN}/${NEXT} ${RUNNING}/${NEXT}
        echo ${active} active, starting ${NEXT}
        ${CMD} ${NEXT} ${RUNNING}/${NEXT} ${OUT}/ > ${LOGS}/${NEXT}.log 2>&1 &
    else
        echo ${active} active, waiting
        sleep 1
    fi
done

while true; do
    active=`ps auxww | fgrep "${CMD}" | wc -l`

    if [ ${active} -eq 1 ]; then    # Account for fgrep
        echo Done.
        exit 0
    else
        echo Waiting on ${active} running jobs
        sleep 5
    fi
done

# End.
