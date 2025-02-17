import time
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ========== CLEAN UP PREVIOUS CHROME SESSIONS ==========
os.system("pkill -f chrome || true")  # Kills any running Chrome instances

# ========== SETUP CHROME DRIVER ==========
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-gpu")

# 🔥 NEW: Ensure a unique user-data directory to prevent conflicts
user_data_dir = tempfile.mkdtemp()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# 🔥 NEW: Run Chrome headless in CI/CD environments (Comment out if debugging locally)
chrome_options.add_argument("--headless")

# ========== INITIALIZE CHROME DRIVER ==========
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # ========== NAVIGATE TO TARGET WEBSITE ==========
    url = "https://www.example.com"  # Change this to the target website
    driver.get(url)

    print(f"✅ Successfully opened {url}")
    print("Page Title:", driver.title)

    # ========== WAIT FOR AN ELEMENT TO LOAD ==========
    try:
        wait = WebDriverWait(driver, 10)  # Max wait time: 10 sec
        element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))  # Adjust selector as needed
        print(f"🎯 Found element: {element.text}")
    except Exception as e:
        print(f"⚠️ Element not found: {e}")

    # ========== SCREENSHOT (Optional Debugging) ==========
    screenshot_path = "screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"📸 Screenshot saved: {screenshot_path}")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    # ========== CLOSE DRIVER ==========
    driver.quit()
    print("🚀 Chrome session closed successfully.")
