import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --------------------- Setup Selenium WebDriver --------------------- #
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Ensures modern headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-browser-side-navigation")

    # Set user-agent to mimic a real browser
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Set a large window size
    driver.set_window_size(1920, 1080)

    return driver

# --------------------- Extract Report Data --------------------- #
def scrape_facebook_report(driver, report_url):
    print("Accessing the page...")
    driver.get(report_url)

    try:
        print("Waiting for the report table to load...")
        table = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        # Take screenshot for debugging
        driver.save_screenshot("table_loaded.png")

        # Save page source for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print("Extracting table data...")

        # Extract data from table
        rows = table.find_elements(By.TAG_NAME, "tr")
        extracted_data = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            row_data = [col.text.strip() for col in cols]
            if row_data:  # Ensure empty rows are ignored
                extracted_data.append(row_data)

        print(f"Extracted {len(extracted_data)} rows.")

        return extracted_data

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# --------------------- Save Data to CSV --------------------- #
def save_to_csv(data, filename="facebook_report.csv"):
    if not data:
        print("No data to save.")
        return

    headers = ["Campaign Name", "Ad Set Name", "Date", "Results", "Amount Spent", "Cost per Result"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Writing header row
        writer.writerows(data)

    print(f"Data saved to {filename}.")

# --------------------- Main Execution --------------------- #
if __name__ == "__main__":
    REPORT_URL = os.getenv("REPORT_URL")

    if not REPORT_URL:
        print("ERROR: REPORT_URL environment variable is missing.")
        exit(1)

    driver = setup_driver()

    try:
        extracted_data = scrape_facebook_report(driver, REPORT_URL)
        save_to_csv(extracted_data)
    finally:
        print("Closing the browser...")
        driver.quit()
