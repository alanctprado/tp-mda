import csv
import json
import os
import consts.fields as fields

directory = './data/submissions'
header = fields.submission

with open('submissions.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header, delimiter="\t")
    writer.writeheader()
    for json_file in os.listdir(directory):
        handle = json_file[:-5]
        with open(os.path.join(directory, json_file), 'r') as f:
            data = json.load(f)
            for item in data:
                row_data = item.copy()
                row_data["handle"] = handle
                writer.writerow(row_data)