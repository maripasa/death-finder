import logging
from typing import List, Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from services.driver import Driver
from services.progress import ProgressBar
from services.document import read_csv, validate_csv_path, determine_output_path, write_json

FRAMINGHAM_URL = "https://www.mdcalc.com/calc/38/framingham-risk-score-hard-coronary-heart-disease"

"""
CHANGE THE FOLLOWING TABLE TO FIT YOUR DATASET
"""

FRAMINGHAM_INPUTS = {
    "age": "person_age_years",
    "cholesterol": "COLESTEROL_TOTAL",
    "hdl_cholesterol": "HDL",
    "systolic_bp" : "PRESSAO_ARTERIAL_PAS",
}
FRAMINGHAM_BUTTONS = {
    "sex": {
        "alias": "sex",
        "uppercase_truth_value": "MASCULINO"
        },
    "smoker": {
        "alias": "smoking",
        "uppercase_truth_value": "TRUE"
        },
    "blood_pressure": {
        "alias": "regular_use_of_medication",
        "uppercase_truth_value": "TRUE"
        },
}

FRAMINGHAM_VALIDATION_RULES = [
    lambda line: 30 < float(line["person_age_years"]) < 79,
    lambda line: 40 < float(line["COLESTEROL_TOTAL"]) < 1000,
    lambda line: 1 < float(line["HDL"]) < 155,
    lambda line: 30 < float(line["PRESSAO_ARTERIAL_PAS"]) < 300,
]

class DeathFinder:
    """Handles the calculation logic for Framingham and LIN calculators."""

    def __init__(self, args):
        self.driver = Driver(debug=args.debug).driver
        self.input_path: str = args.csv
        self.calculator: str = args.calculator
        self.output_path: str = args.output
        self.output_file = determine_output_path(self.output_path)
        self.wait = args.wait
        self.last_pressed = {}

        if args.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                filename="logs.log",
            )

    def extract_csv_for_framingham(self) -> List[Dict]:
        """Extracts and validates data from the CSV file for Framingham calculations."""
        validate_csv_path(self.input_path)
        data = read_csv(self.input_path)

        processed_data = []
        for line in data:
            valid = all(line[key] != "" for key in {value for value in FRAMINGHAM_BUTTONS.keys()}
                        .union({value for value in FRAMINGHAM_INPUTS.keys()})) and \
                        all(rule(line) for rule in FRAMINGHAM_VALIDATION_RULES
            )
            
            buttons = {
                key: str(int(line[FRAMINGHAM_BUTTONS[key]["alias"]].upper() == FRAMINGHAM_BUTTONS[key]["uppercase_truth_value"]))
                for key in FRAMINGHAM_BUTTONS.keys()
            }
            inputs = {key: line[FRAMINGHAM_INPUTS[key]] for key in FRAMINGHAM_INPUTS.keys()}

            processed_data.append(
                {
                    "valid": valid,
                    **buttons,
                    **inputs,
                }
            )

        return processed_data

    def calculate_framingham(self) -> None:
        """Performs the Framingham calculation using Selenium."""
        data = self.extract_csv_for_framingham()
        result = []
        
        progress_bar = ProgressBar()

        try:
            self.driver.get(FRAMINGHAM_URL)
            self.driver.execute_script("document.body.style.zoom='0.6'")

            progress_bar.update(0, len(data))

            for i, sample in enumerate(data):

                progress_bar.sample_time()

                if not sample["valid"]:
                    result.append([None, None])
                    continue

                self._fill_inputs_framingham(sample)
                self._click_buttons_framingham(sample)
                
                try:
                    WebDriverWait(self.driver, round(self.wait/10, 1)).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "[class*='calc_loading']"))
                    )

                    WebDriverWait(self.driver, self.wait).until(
                        EC.invisibility_of_element_located((By.CSS_SELECTOR, "[class*='calc_loading']"))
                    )
                    
                except Exception as e:
                    logging.warning(f"Failed to find calc_loading {e}")

                h2_1 = WebDriverWait(self.driver, self.wait).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "[class*='calc_result-list'] div:nth-child(1) h2"))
                )
                h2_2 = WebDriverWait(self.driver, self.wait).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "[class*='calc_result-list'] div:nth-child(2) h2"))
                )
                
                value_1 = h2_1.text.replace("%", "").replace("<", "").strip()
                value_2 = h2_2.text.replace("%", "").replace("<", "").strip()

                result.append(
                    [
                        float(value_1) if value_1 != "" else None,
                        float(value_2) if value_2 != "" else None
                    ]
                )

                progress_bar.update(i + 1, len(data))

        except Exception as e:
            logging.error(f"Error during scraping: {e}", exc_info=True)
            raise
        finally:
            self.driver.quit()

        write_json(result, self.output_file)

    def _fill_inputs_framingham(self, sample: Dict) -> None:
        """Fills input fields on the Framingham calculator page."""
        inputs = ["age", "cholesterol", "hdl_cholesterol", "systolic_bp"]
        for input_name in inputs:
            element = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located((By.NAME, input_name))
            )
            element.clear()
            element.send_keys(sample[input_name])
            logging.debug(f"Filled input {input_name} with value {sample[input_name]}")

    def _click_buttons_framingham(self, sample: Dict) -> None:
        """Clicks buttons on the Framingham calculator page."""
        buttons = ["sex", "smoker", "blood_pressure"]
        for button_name in buttons:
            if self.last_pressed.get(button_name, "") == sample[button_name]:
                continue

            element = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"input[name='{button_name}'][value='{sample[button_name]}']"))
            )
            self.driver.execute_script("arguments[0].click();", element)
            self.last_pressed[button_name] = sample[button_name]
            logging.debug(f"Clicked button {button_name} with value {sample[button_name]}")

    def calculate_lin(self) -> None:
        pass

    def calculate(self) -> None:
        """Runs the appropriate calculator based on the user's choice."""
        if self.calculator == "framingham":
            self.calculate_framingham()
            return

        if self.calculator == "lin":
            self.calculate_lin()
            return

        raise ValueError(f"Invalid calculator: {self.calculator}")
