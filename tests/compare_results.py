import json
import argparse
import os

parser = argparse.ArgumentParser(
    prog="Compare Jsons",
)

parser.add_argument("first", help="First Json")
parser.add_argument("second", help="Second Json")

args = parser.parse_args()

if not os.path.exists(args.first):
   raise FileNotFoundError(args.first)

if not os.path.exists(args.second):
   raise FileNotFoundError(args.second)

result = True

with open(args.first, 'r') as file:
    data_first = json.load(file)

with open(args.second, 'r') as file:
    data_second = json.load(file)

for value in range(min(len(data_first), len(data_second))):
    if data_first[value] != data_second[value]:
        print(f"{value}: ", data_first[value], data_second[value])
        result = False

if len(data_first) != len(data_second):
    print("Different Sizes")
    result = False


