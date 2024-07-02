#!/usr/bin/sh

if [ -z "$1" ]; then echo "Usage: $0 <true|false>"; exit 1; fi

arg=$1
if [ "$arg" = "true" ]; then get_users="true"
elif [ "$arg" = "false" ]; then get_users=""
else echo "Invalid argument. Please use 'true' or 'false'."; exit 1; fi

if [ -d "venv" ]; then source venv/bin/activate; fi

if [ ! -f "data/users.txt" ] || [ -n "$get_users" ]; then
    echo "Fetching data from Codeforces, please wait..."
    python3 get_contests.py
    cat data/contests/*users.txt | sort -u > data/users.txt
fi

echo "Found $(wc -l data/users.txt | cut -d' ' -f1) unique users!"

split -l 500 data/users.txt chunk_

for chunk in chunk_*
do
    echo "Processing $chunk"
    users=$(tr '\n' ';' < "$chunk" | sed 's/.$//')
    python3 get_users.py "$users"
    sleep 2
done

rm chunk_*

if [ -d "venv" ]; then deactivate; fi
