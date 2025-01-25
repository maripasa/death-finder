import json
import argparse
import os

parser = argparse.ArgumentParser(
    prog="Reduce to floats and Nones the json",
)

parser.add_argument("json", help="Json to be filtered")

args = parser.parse_args()

if not os.path.exists(args.json):
   raise FileNotFoundError(args.json)

with open(args.json, 'r') as file:
    data = json.load(file)

filtered_data = []
for sample in data:
    value_1 = data[0].text.replace("%", "").replace("<", "").strip()
    value_2 = data[1].text.replace("%", "").replace("<", "").strip()
    filtered_data.append(
        [
            float(value_1) if value_1 != "" else None,
            float(value_2) if value_2 != "" else None
        ]
    )

with open(args.json, 'w') as file:
    json.dump({}, file)

with open(args.json, "w") as file:
    json.dump(filtered_data, file, indent=4)
