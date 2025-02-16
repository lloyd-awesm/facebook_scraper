import os
import time
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Load environment variables
load_dotenv()
FB_USERNAME = os.getenv("FB_USERNAME")
FB_PASSWORD = os.getenv("FB_PASSWORD")
REPORT_URL = os.getenv("REPORT_URL")

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# 🚨 Temporary: Disable headless mode for debugging (Uncomment if needed)
# chrome_options.add_argument("--headless=new")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    logging.info("Accessing the page...")
    driver.get(REPORT_URL)

    # Handle Facebook Login if needed
    if FB_USERNAME and FB_PASSWORD:
        try:
            logging.info("Attempting to log in to Facebook...")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(FB_USERNAME)
            driver.find_element(By.ID, "pass").send_keys(FB_PASSWORD)
            driver.find_element(By.NAME, "login").click()
            logging.info("Login submitted, waiting for redirection...")
            time.sleep(5)  # Allow time for login redirection
        except NoSuchElementException:
            logging.warning("Login fields not found. Skipping login step.")

    # Wait for the report table to load
    try:
        logging.info("Waiting for the report table to load...")
        table = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        logging.info("Report table found, extracting data...")
        
        # Extract table content
        table_html = table.get_attribute("outerHTML")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(table_html)

    except TimeoutException:
        logging.error("Timed out waiting for the report table.")
        raise

except Exception as e:
    logging.error(f"Error occurred: {e}")

finally:
    logging.info("Closing the browser...")
    driver.quit()
