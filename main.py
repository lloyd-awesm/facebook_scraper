import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Get the URL from environment variable
url = os.environ.get("REPORT_URL", "https://default.url.com")

def setup_driver():
    """Setup and return a Selenium WebDriver with headless Chrome options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Modern headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-browser-side-navigation")

    # Mimic a real browser to prevent blocking
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Set a large window size
    driver.set_window_size(1920, 1080)

    return driver

def parse_and_save_to_csv(text_content):
    """Extract data from the scraped text and save it to CSV."""
    lines = text_content.split("\n")
    data = []
    main_campaign = "B - Hypopressiv Trening - BOF - Leads - NO"
    current_campaign = ""
    current_adset = ""

    for i, line in enumerate(lines):
        if "BOF - Leads" in line and not any(x in line for x in ["kr", "Website leads"]):
            if any(x in line for x in ["Website Visitors", "T1", "T2", "T3", "T4"]):
                current_adset = line.strip()
                current_campaign = main_campaign
            else:
                current_campaign = line.strip()
                current_adset = line.strip()

        if line.startswith("2025-") or line == "All":
            results, amount, cost = "", "", ""

            for j in range(i+1, min(i+8, len(lines))):
                line_text = lines[j].strip()

                if not results and any(c.isdigit() for c in line_text):
                    results = next((s for s in line_text.split() if s.isdigit()), "")

                if "kr" in line_text:
                    if not amount:
                        amount = line_text
                    elif not cost and "kr" in line_text and line_text != amount:
                        cost = line_text
                        break

            if current_campaign and (results or amount or cost):
                data.append([current_campaign, current_adset, line.strip(), results, amount, cost])

    if data:
        df = pd.DataFrame(data, columns=["Campaign name", "Ad Set Name", "Day", "Results", "Amount spent", "Cost per result"])
        file_path = "facebook_report.csv"
        df.to_csv(file_path, index=False)

        print(f"CSV file saved at: {os.path.abspath(file_path)}")
        print(f"\nSaved {len(df)} rows to facebook_report.csv")
        print("\nFirst few rows:")
        print(df.head())

        return df
    return None

def scrape_facebook_report(url):
    """Scrape Facebook Ads report and save extracted data to CSV."""
    driver = setup_driver()
    try:
        print("Accessing the page...")
        driver.get(url)

        # Ensure the table is fully loaded
        print("Waiting for the report table to load...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(5)  # Additional wait to ensure data loads

        # Scroll down multiple times to trigger lazy loading
        print("Scrolling page to load all data...")
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Take a final screenshot
        driver.save_screenshot("final_stage.png")
        print("Final screenshot saved as final_stage.png")

        # Save the full page HTML for debugging
        page_source = driver.page_source
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        print("Saved full HTML source.")

        # Extract all div elements for text processing
        all_divs = driver.find_elements(By.TAG_NAME, "div")
        print(f"Found {len(all_divs)} div elements")

        longest_content = ""
        content_found = 0

        for div in all_divs:
            try:
                text = div.text
                if "BOF - Leads" in text:
                    content_found += 1
                    print(f"Found content block {content_found}, length: {len(text)}")
                    if len(text) > len(longest_content):
                        longest_content = text
            except Exception as e:
                print(f"Error processing div: {e}")

        if longest_content:
            print(f"Extracting data from the longest content block ({len(longest_content)} characters).")
            return parse_and_save_to_csv(longest_content)
        else:
            print("No relevant content found.")
            return None

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Closing the browser...")
        driver.quit()

if __name__ == "__main__":
    df = scrape_facebook_report(url)
