from collections import defaultdict
import csv
import json
import pandas as pd
import os
import consts.fields as fields

directory = './data/users' # Change here
header = fields.user # Change here 

with open('output.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header)

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename)) as f:
            data = json.load(f)
            data = defaultdict(lambda: 'missing', data)
            with open('output.csv', 'a', newline='') as output_file:
                writer = csv.writer(output_file)
                writer.writerow([data[field] for field in header])