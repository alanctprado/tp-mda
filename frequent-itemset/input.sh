#!/usr/bin/sh

PROJECT_DIR=$(realpath $(dirname $0)/..)
SUBMISSIONS_DIR=$PROJECT_DIR/data/submissions

source $PROJECT_DIR/venv/bin/activate

touch map.txt
touch result.txt
num_files="$(ls ${SUBMISSIONS_DIR} | wc -l)"

i=0
for user in $SUBMISSIONS_DIR/*
do
    handle=$(sed 's:.*\/submissions\/\(.*\)\.json:\1:' <<< $user)
    echo -n "user$i " >> result.txt
    python3 input_script.py $user >> result.txt
    i=$((i+1))
    echo "user$i $handle" >> map.txt
    echo $handle
done | tqdm --total=$num_files >> /dev/null
