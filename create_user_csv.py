from collections import defaultdict
import csv
import json
import os
import consts.fields as fields

directory = './data/users'
header = fields.user

with open('output.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header)

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename), encoding='utf-8') as f:
            data = json.load(f)
            data = defaultdict(lambda: '', data)
            with open('output.csv', 'a', newline='') as output_file:
                writer = csv.writer(output_file)
                writer.writerow([data[field] for field in header])