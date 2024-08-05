#!/usr/bin/sh

if [ ! -f "$MDADATADIR/contests" ] ; then
    echo "Fetching data from Codeforces, please wait..."
    python get_contests.py
fi

cat $MDADATADIR/contests/*users.txt | sort -u > $MDADATADIR/users.txt

echo "Found $(wc -l "$MDADATADIR/users.txt" | cut -d' ' -f1) unique users!"

split -l 500 "$MDADATADIR/users.txt chunk_"

for chunk in chunk_*
do
    echo "Processing $chunk"
    users=$(tr '\n' ';' < "$chunk" | sed 's/.$//')
    python3 get_users.py "$users"
    sleep 2
done

rm chunk_*

if [ -d "venv" ]; then deactivate; fi
