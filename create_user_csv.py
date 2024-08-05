from collections import defaultdict
import csv
import json
import os
import consts.fields as fields

directory = './data/users'
header = fields.user

output_file = open('output.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(output_file, delimiter="\t")
writer.writerow(header)
    

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename), encoding='utf-8') as f:
            data = json.load(f)
            data = defaultdict(lambda: '', data)
            print(data)
            writer.writerow([data[field] for field in header])