from selenium.webdriver.common.by import By
from services.driver import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import json
import logging
import time
from typing import List, Dict

# Constants
FRAMINGHAM_URL = "https://www.mdcalc.com/calc/38/framingham-risk-score-hard-coronary-heart-disease"
FRAMINGHAM_NECESSARY_DATA = [
    "person_age_years",
    "sex",
    "smoking",
    "COLESTEROL_TOTAL",
    "HDL",
    "PRESSAO_ARTERIAL_PAS",
    "regular_use_of_medication",
]
FRAMINGHAM_VALIDATION_RULES = [
    lambda line: 30 < float(line["person_age_years"]) < 79,
    lambda line: 40 < float(line["COLESTEROL_TOTAL"]) < 1000,
    lambda line: 1 < float(line["HDL"]) < 155,
    lambda line: 30 < float(line["PRESSAO_ARTERIAL_PAS"]) < 300,
]

class DeathFinder:
    def __init__(self, args):
        self.driver = Driver(debug=args.debug).driver
        self.input_path: str = args.csv
        self.output_path: str = args.output
        self.is_only_framingham: bool = args.framingham
        self.is_only_lin: bool = args.lin
        self.output_file = self.determine_output_file()

        if args.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                filename="selenium.log",
            )

    def extract_csv_for_framingham(self) -> List[Dict]:
        data = []
        self.check_csv_path()

        with open(self.input_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for line in csv_reader:
                valid = all(line[key] != '' for key in FRAMINGHAM_NECESSARY_DATA) and \
                        all(rule(line) for rule in FRAMINGHAM_VALIDATION_RULES)

                data.append({
                    "valid": valid,
                    "age": line["person_age_years"],
                    "sex": "1" if line["sex"].upper() == "MASCULINO" else "0",
                    "smoker": "1" if line["smoking"].upper() == "TRUE" else "0",
                    "cholesterol": line["COLESTEROL_TOTAL"],
                    "hdl_cholesterol": line["HDL"],
                    "systolic_bp": line["PRESSAO_ARTERIAL_PAS"],
                    "blood_pressure": "1" if line["regular_use_of_medication"].upper() == "TRUE" else "0"
                })

        return data

    def calculate_framingham(self):
        data = self.extract_csv_for_framingham()
        result = []
        self.last_pressed = {}

        try:
            self.driver.get(FRAMINGHAM_URL)
            
            self.driver.execute_script("document.body.style.zoom='0.6'")

            for sample in data:
                if not sample["valid"]:
                    result.append(["", ""])
                    continue

                self._fill_inputs_framingham(sample)
                self._click_buttons_framingham(sample)

                time.sleep(1)

                h2_1 = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "[class*='calc_result-list'] div:nth-child(1) h2"))
                )

                h2_2 = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "[class*='calc_result-list'] div:nth-child(2) h2"))
                )

                result.append([h2_1.text, h2_2.text])

        except Exception as e:
            logging.error(f"Error during scraping: {e}", exc_info=True)
            raise
        finally:
            self.driver.quit()
        self._write_output(result)

    def _fill_inputs_framingham(self, sample: Dict):
        inputs = ["age", "cholesterol", "hdl_cholesterol", "systolic_bp"]
        for input_name in inputs:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, input_name))
            )
            element.clear()
            element.send_keys(sample[input_name])
            logging.debug(f"Filled input {input_name} with value {sample[input_name]}")

    def _click_buttons_framingham(self, sample: Dict):
        buttons = ["sex", "smoker", "blood_pressure"]
        for button_name in buttons:

            if self.last_pressed.get(button_name, "") == sample[button_name]:
                continue

            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"input[name='{button_name}'][value='{sample[button_name]}']"))
            )
            
            self.driver.execute_script("arguments[0].click();", element)
            self.last_pressed[button_name] = sample[button_name]
            logging.debug(f"Clicked button {button_name} with value {sample[button_name]}")

    def _write_output(self, result: List[List[str]]):
        with open(self.output_file, 'w') as f:
            json.dump(result, f)
        logging.info(f"Results written to {self.output_file}")

    def check_csv_path(self):
        if not (self.input_path.endswith(".csv") and os.path.exists(self.input_path)):
            logging.error(f"Invalid CSV path: {self.input_path}")
            raise FileNotFoundError(f"Invalid CSV path: {self.input_path}")

    def determine_output_file(self) -> str:
        if os.path.isdir(self.output_path):
            return os.path.join(self.output_path, "output.json")
        if not self.output_path.endswith(".json"):
            logging.error(f"Output path must be a JSON file: {self.output_path}")
            raise ValueError(f"Output path must be a JSON file: {self.output_path}")
        return self.output_path

    def calculate_lin(self):
        pass

    def calculate(self):
        if self.is_only_lin:
            self.calculate_lin()
        elif self.is_only_framingham:
            self.calculate_framingham()
