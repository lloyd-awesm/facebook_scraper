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

# *** REMOVE HEADLESS FOR DEBUGGING ***
# Comment this out if you want to debug visually
# chrome_options.add_argument("--headless=new")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ========== LOAD WEBPAGE ==========
URL = "https://www.example.com"  # CHANGE THIS TO YOUR ACTUAL URL
driver.get(URL)

# ========== WAIT FOR PAGE TO LOAD ==========
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Page loaded successfully.")
except:
    print("❌ Page failed to load.")

# ========== SCROLL TO LOAD CONTENT ==========
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)  # Allow content to load

# ========== TAKE FINAL SCREENSHOT ==========
screenshot_path = "final_stage.png"
driver.save_screenshot(screenshot_path)
print(f"✅ Screenshot saved: {screenshot_path}")

# ========== DEBUG: SAVE PAGE SOURCE ==========
with open("debug_page_source.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)
print("✅ Page source saved for debugging.")

# ========== CLOSE BROWSER ==========
driver.quit()
