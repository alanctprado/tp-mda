#!/usr/bin/sh

if [ ! -d "$MDADATADIR/submissions" ]
then
    mkdir "$MDADATADIR/submissions"
fi

num_files="$(ls ${MDADATADIR}/active_users | wc -l)"

for user in $MDADATADIR/active_users/*
do
    handle=$(sed 's:.*\/active_users\/\(.*\)\.json:\1:' <<< $user)
    echo $handle
    if [ ! -f $MDADATADIR/submissions/$handle.json ]
    then
        python3 $MDASCRIPTDIR/get_submissions.py $handle ../data/submissions 2>&1 /dev/null
        sleep 2
    fi
done | tqdm --total=$num_files >> /dev/null
