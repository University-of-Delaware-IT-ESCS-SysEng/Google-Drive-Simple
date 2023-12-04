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

CMD='/home/mike/work/gd-run/doit.sh'
IN='/home/mike/work/gd-run/in'
OUT='/home/mike/work/gd-run/out'
RUNNING='/home/mike/work/gd-run/running'
LOGS='/home/mike/work/gd-run/logs'
MAX=75

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
