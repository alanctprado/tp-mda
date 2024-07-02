#!/usr/bin/sh

export MDABASEDIR=/home/alan/tp-mda/

if [ -d "venv" ]; then source ../venv/bin/activate; fi

if [ ! -d "../data/submissions" ]; then mkdir ../data/submissions; fi

num_files="$(ls $MDABASEDIR/data/active_users | wc -l)"
echo $num_files

for user in ../data/active_users/*
do
    handle=$(echo $user | sed 's:..\/data\/active_users\/\(.*\)\.json:\1:')
    if [ ! -f ../data/submissions/$handle.json ]
    then
        python3 get_submissions.py $handle ../data/submissions
        sleep 2
    fi
    echo "DONE"
done | tqdm --total=$num_files >> /dev/null

if [ -d "venv" ]; then deactivate; fi
