import json
import csv


def json_to_csv(input_file, output_file):
    with open(input_file) as data_file:
        data = json.load(data_file)
    
    with open(output_file, "w", newline="") as csvfile:
        cw = csv.writer(csvfile)
        cw.writerow(data["headers"])
        # if the JSON contains rows under the key "rows", write them too
        for row in data.get("rows", []):
            cw.writerow(row)
    print(f"CSV written to {output_file}")