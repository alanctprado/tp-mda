#!/usr/bin/sh

if [ ! -d "$MDADATADIR/contests" ]
then
    echo "Fetching data from Codeforces, please wait..."
    python "$MDASCRIPTDIR/get_contests.py"
fi

sort -u $MDADATADIR/contests/*users.txt > $MDADATADIR/users.txt

echo "Found $(wc -l "$MDADATADIR/users.txt" | cut -d' ' -f1) unique users!"

split -l 500 "$MDADATADIR/users.txt" "$MDADATADIR/chunk_"

for chunk in $MDADATADIR/chunk_*
do
    echo "Processing $chunk"
    users=$(tr '\n' ';' < "$chunk" | sed 's/.$//')
    python3 "$MDASCRIPTDIR/get_users.py" "$users"
    # sleep 2
done

rm $MDADATADIR/chunk_*
