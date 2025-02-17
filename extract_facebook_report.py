from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import traceback
import time

def setup_driver():
    """Set up the Chrome WebDriver with necessary options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (important for GitHub Actions)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  # Recommended for CI/CD environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_facebook_report(url):
    """Scrapes the Facebook report page and extracts relevant data."""
    driver = setup_driver()
    
    try:
        print("🔍 Accessing the page...")
        driver.get(url)
        time.sleep(5)  # Wait for elements to load

        # Implement actual scraping logic here (example)
        # Example: Extracting a table if it's on the page
        tables = pd.read_html(driver.page_source)
        df = tables[0] if tables else pd.DataFrame()

        # Save results
        df.to_csv("facebook_report.csv", index=False)
        print(f"✅ Saved {len(df)} rows to facebook_report.csv")

        # Capture a screenshot for debugging
        driver.save_screenshot("final_state.png")
        print("📸 Saved screenshot")

        return df

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print(traceback.format_exc())

    finally:
        if 'driver' in locals():  # Ensures driver is closed properly
            driver
