import csv
import argparse
import os
import json

parser = argparse.ArgumentParser(
    prog="Manual Result Generation Helper",
)

def check_csv_path(input_path: str):
    if not (input_path.endswith(".csv") and os.path.exists(input_path)):
        raise FileNotFoundError(f"Invalid CSV path: {input_path}")

parser.add_argument("csv", help="Csv to generate results from.")

args = parser.parse_args()

if not os.path.exists(args.csv):
   raise FileNotFoundError(args.csv)

data = []
check_csv_path(args.csv)

with open(args.csv, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for line in csv_reader:
        data.append({
            "age": line["person_age_years"],
            "sex": "Male" if line["sex"].upper() == "MASCULINO" else "Female",
            "smoker": "Yes" if line["smoking"].upper() == "TRUE" else "No",
            "cholesterol": line["COLESTEROL_TOTAL"],
            "hdl_cholesterol": line["HDL"],
            "systolic_bp": line["PRESSAO_ARTERIAL_PAS"],
            "blood_pressure": "Yes" if line["regular_use_of_medication"].upper() == "TRUE" else "No"
        })

results = []


index = 1
for sample in data:
    os.system('clear')

    print(f"Number {index}")
    for key, item in sample.items():
        print(key, ": ", item)

    results.append([
        str(input(
            "\nFirst: "
            )),
        str(input(
            "\nSecond: "
                ))])

    index += 1


num = 0
while os.path.exists(output := f"manual_output{num}.json"):
    num += 1

with open(output, 'w') as f:
    json.dump(results, f)
