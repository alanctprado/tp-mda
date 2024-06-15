#!/usr/bin/sh

if [ -z "$1" ]; then echo "Usage: $0 <true|false>"; exit 1; fi

arg=$1
if [ "$arg" = "true" ]; then get_users=true
elif [ "$arg" = "false" ]; then get_users=false
else echo "Invalid argument. Please use 'true' or 'false'."; exit 1; fi

if [ -d "venv" ]; then source venv/bin/activate; fi

if [ ! -f "data/users.txt" ] || [ $get_users ]; then
    echo "Fetching data from Codeforces, please wait..."
    python3 get_contests.py
    cat data/contests/*users.txt | sort -u > data/users.txt
fi

echo "Found $(wc -l data/users.txt | cut -d' ' -f1) unique users!"

if [ -d "venv" ]; then deactivate; fi
