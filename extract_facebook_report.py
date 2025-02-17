import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_facebook_report(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.add_argument("--remote-debugging-port=9222")  

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)
        print("🔍 Accessing the page...")
        time.sleep(5)

        # ✅ Print current working directory
        cwd = os.getcwd()
        print(f"📂 Current Directory: {cwd}")

        # ✅ Force Screenshot Save in Different Ways
        screenshot_path = os.path.join(cwd, "page_loaded.png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot attempt 1: {screenshot_path}")

        driver.save_screenshot("./page_loaded_2.png")
        print("📸 Screenshot attempt 2: page_loaded_2.png")

        driver.save_screenshot(os.path.expanduser("~/page_loaded_3.png"))
        print("📸 Screenshot attempt 3: ~/page_loaded_3.png")

        # ✅ Verify if screenshots exist
        for filename in ["page_loaded.png", "page_loaded_2.png", os.path.expanduser("~/page_loaded_3.png")]:
            if os.path.exists(filename):
                print(f"✅ Screenshot saved successfully: {filename}")
            else:
                print(f"❌ Screenshot NOT found: {filename}")

        # Dummy Data for Testing
        data = {
            "Campaign": ["Test Campaign 1", "Test Campaign 2"],
            "Spend": [100, 200]
        }
        df = pd.DataFrame(data)

        # ✅ Print extracted data before saving
        print("🔍 Extracted Data:")
        print(df.head())

        # Save the updated CSV
        df.to_csv("facebook_report.csv", index=False)
        print("✅ Saved updated facebook_report.csv")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()
        print("Browser closed successfully.")

if __name__ == "__main__":
    url = "https://www.facebook.com/adsviewreport/?saved_report_id=120216194126900650&client_creation_value=f54f992787004415e"
    scrape_facebook_report(url)
