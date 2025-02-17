import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ========== SETUP CHROME DRIVER ==========
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")  # Running in a non-GUI environment

# Start WebDriver
print("🚀 Starting Chrome WebDriver...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    url = "https://www.facebook.com/adsviewreport/?saved_report_id=120216194126900650&client_creation_value=f54f992787004415e"  # Change to actual target URL
    print(f"🌍 Navigating to {url}...")
    driver.get(url)

    # Wait for an element to confirm the page is loaded
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "your_xpath_here")))

    print("✅ Page loaded successfully!")

    # Save page source for debugging
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("📄 Saved page source to page_source.html")

    # Extract data and save to CSV
    # (Replace this with your actual data extraction code)
    extracted_data = "dummy_data"
    with open("facebook_report.csv", "w", encoding="utf-8") as f:
        f.write("header1,header2\n")
        f.write(f"{extracted_data},updated\n")
    print("📊 Data extracted and saved to facebook_report.csv")

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    driver.quit()
    print("🚀 Chrome session closed successfully.")
