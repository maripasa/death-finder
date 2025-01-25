from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Driver: 
    def __init__(self, debug: bool = False):
        """
        Initialize the headless browser.
        :param driver_path: Path to the ChromeDriver executable.
        """
        options = Options()
        
        if debug:
            options.add_argument("--log-level=3")

        if not debug:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
