import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_facebook_report(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging support

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(url)
        print("🔍 Accessing the page...")
        time.sleep(5)  # Allow page to load

        # 📸 Save screenshot to verify page load (even in headless mode)
        driver.save_screenshot("page_loaded.png")
        print("📸 Saved screenshot of the page load")

        # Dummy Data for Testing (Replace with actual scraping logic)
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
