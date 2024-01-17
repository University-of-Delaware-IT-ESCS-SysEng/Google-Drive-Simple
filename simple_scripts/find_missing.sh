#!/bin/bash
BASE="./gd-reports"
GDUSER=${1}
cd ${BASE}/${GDUSER}
sa_output=`mktemp sa_output_XXXXXX`
sa_r_output=`mktemp sa_r_output_XXXXXX`

#
# Because sa and sa_r take a good deal
# of time to run, we should skip files
# that could have been created during
# time dates inbetween runs.  We don't
# have to get that accurate here.  If you
# have missing files at your school, you
# will find them by the millions in
# affected accounts.
#

DATE_TO_SKIP='Time":"2024-01-16'

cut -d: -f 1 ${GDUSER}.json | sort > ${sa_output}
fgrep '"ownedByMe":true' ${GDUSER}-r.json | \
    fgrep -v ''${DATE_TO_SKIP}'' | \
    cut -d: -f 1 | \
    sort > ${sa_r_output}
diff -u ${sa_output} ${sa_r_output} | grep "^+" | \
    cut -d+ -f2 | \
    sed -e '/^$/d' > ${GDUSER}-missing.ids
rm ${sa_output}
rm ${sa_r_output}
