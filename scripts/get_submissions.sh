#!/usr/bin/sh

export MDABASEDIR=/home/alanp/tp-mda/

if [ ! -d "../data/submissions" ]; then mkdir ../data/submissions; fi

num_files="$(ls ${MDABASEDIR}data/active_users | wc -l)"

for user in ../data/active_users/*
do
    handle=$(echo $user | sed 's:..\/data\/active_users\/\(.*\)\.json:\1:')
    echo $handle
    if [ ! -f ../data/submissions/$handle.json ]
    then
        python3 get_submissions.py $handle ../data/submissions 2>&1 /dev/null
        sleep 2
    fi
done | tqdm --total=$num_files >> /dev/null
