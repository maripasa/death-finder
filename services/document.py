import csv
import json
import os
import logging
from typing import List, Dict

"""Handles file operations such as validation, reading, and writing."""

def validate_csv_path(input_path: str) -> None:
    """Validates the CSV file path."""
    if not input_path.endswith(".csv"):
        raise ValueError(f"Invalid file type: {input_path}. Expected a .csv file.")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

def determine_output_path(output_path: str) -> str:
    """Determines the output file path. Defaults to './output.json' if output_path is a directory."""
    if os.path.isdir(output_path):
        return os.path.join(output_path, "output.json")
    if not output_path.endswith(".json"):
        raise ValueError(f"Output path must be a JSON file: {output_path}")
    return output_path

def read_csv(input_path: str) -> List[Dict]:
    """Reads a CSV file and returns its contents as a list of dictionaries."""
    with open(input_path, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def write_json(data: List, output_path: str) -> None:
    """Writes data to a JSON file."""
    with open(output_path, "w") as file:
        json.dump(data, file, indent=4)
    logging.info(f"Results written to {output_path}")

