import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re

# Get the URL from environment variable
url = os.environ.get('REPORT_URL', 'default_url_if_not_set')

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-browser-side-navigation")
    
    # Add these new parameters
    prefs = {
        "profile.default_content_setting_values.cookies": 2,
        "profile.block_third_party_cookies": True,
        "profile.default_content_settings.popups": 0,
        "profile.default_content_settings.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Clear cache and cookies
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})
    driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
    
    return driver

def parse_and_save_to_csv(text_content):
    lines = text_content.split('\n')
    data = []
    main_campaign = "B - Hypopressiv Trening - BOF - Leads - NO"
    current_campaign = ""
    current_adset = ""
    
    for i, line in enumerate(lines):
        # If line contains campaign info
        if "BOF - Leads" in line and not any(x in line for x in ['kr', 'Website leads']):
            if "Website Visitors" in line or "T1" in line or "T2" in line or "T3" in line or "T4" in line:
                current_adset = line.strip()
                current_campaign = main_campaign
            else:
                current_campaign = line.strip()
                current_adset = line.strip()
        
        # If line is a date or "All", it's a data row
        if line.startswith('2025-') or line == 'All':
            results = ""
            amount = ""
            cost = ""
            
            # Look ahead for values
            for j in range(i+1, min(i+8, len(lines))):
                line_text = lines[j].strip()
                
                # Get results number
                if not results and any(c.isdigit() for c in line_text):
                    results = next((s for s in line_text.split() if s.isdigit()), "")
                
                # Get amount and cost
                if 'kr' in line_text:
                    if not amount:
                        amount = line_text
                    elif not cost and 'kr' in line_text and line_text != amount:
                        cost = line_text
                        break
            
            if current_campaign and (results or amount or cost):
                data.append([
                    current_campaign,
                    current_adset,
                    line.strip(),  # Day
                    results,
                    amount,
                    cost
                ])
    
    if data:
        df = pd.DataFrame(data, columns=['Campaign name', 'Ad Set Name', 'Day', 'Results', 'Amount spent', 'Cost per result'])
        df.to_csv('facebook_report.csv', index=False)
        print(f"\nSaved {len(df)} rows to facebook_report.csv")
        print("\nFirst few rows:")
        print(df.head())
        return df
    return None

def scrape_facebook_report(url):
    driver = setup_driver()
    try:
        print("Accessing the page...")
        driver.get(url)
        print("Waiting for page to fully load...")
        time.sleep(15)  # Increased wait time
        
        # Scroll to ensure all content is loaded
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Only get the content once
        all_divs = driver.find_elements(By.TAG_NAME, "div")
        longest_content = ""
        
        for div in all_divs:
            try:
                text = div.text
                if "BOF - Leads" in text:
                    # Keep the longest content that contains our data
                    if len(text) > len(longest_content):
                        longest_content = text
            except:
                continue
        
        if longest_content:
            print("\nFound relevant content:")
            print(longest_content[:200] + "...")  # Print preview
            return parse_and_save_to_csv(longest_content)
            
        return None

    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        print(traceback.format_exc())
    finally:
        driver.save_screenshot("final_state.png")
        print("Saved screenshot")
        driver.quit()

if __name__ == "__main__":
    df = scrape_facebook_report(url)
