import os
import time
import tempfile
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Create a unique temporary directory for Chrome user data
temp_user_data_dir = tempfile.mkdtemp()
logging.info(f"Using temp user data directory: {temp_user_data_dir}")

# Set up Chrome options for headless execution in GitHub Actions
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={temp_user_data_dir}")  # Fix session conflict
chrome_options.add_argument("--no-sandbox")  # Run Chrome without sandboxing (needed in CI/CD)
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent memory issues
chrome_options.add_argument("--window-size=1920,1080")  # Ensure full-screen mode
chrome_options.add_argument("--headless=new")  # Enable new headless mode

# Initialize WebDriver
logging.info("Initializing Chrome WebDriver...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # URL to scrape (Change this to your target URL)
    target_url = "https://www.example.com"
    logging.info(f"Navigating to {target_url}")
    
    driver.get(target_url)
    time.sleep(3)  # Allow time for page to load
    
    # Example: Scrape page title
    page_title = driver.title
    logging.info(f"Page title: {page_title}")
    
    # Example: Find and extract an element by class name
    element = driver.find_element(By.CLASS_NAME, "some-class-name")  # Change as needed
    logging.info(f"Extracted text: {element.text}")

    # Save page source for debugging
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    logging.info("Saved page source to 'page_source.html'.")

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    # Clean up and close the browser
    logging.info("Closing browser and cleaning up...")
    driver.quit()
