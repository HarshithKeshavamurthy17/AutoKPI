import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_driver():
    """Setup headless Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def check_and_wake_app():
    """Visit the app and click the wake up button if present"""
    app_url = os.environ.get("STREAMLIT_APP_URL")
    if not app_url:
        logger.error("STREAMLIT_APP_URL environment variable not set")
        return

    logger.info(f"Starting keep-alive check for: {app_url}")
    driver = None
    
    try:
        driver = setup_driver()
        driver.get(app_url)
        logger.info("Page loaded successfully")
        
        # Wait for potential content to load
        time.sleep(5)
        
        # Check for the specific "Yes, get this app back up!" button
        # Streamlit's wake up button usually has this text
        xpath = "//button[contains(text(), 'Yes, get this app back up!')]"
        
        try:
            # Short wait for the button since if it's there, it should be there quickly
            # If the app is awake, this will timeout, which is expected
            wait = WebDriverWait(driver, 10)
            button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            if button:
                logger.info("Wake up button found! Clicking it...")
                button.click()
                logger.info("Clicked wake up button")
                
                # Wait a bit to ensure the click registers
                time.sleep(5)
            
        except Exception as e:
            # This is actually good news - it likely means the button wasn't found
            # so the app is probably already awake
            logger.info("Wake up button not found - App is likely already awake")
            
            # Optional: Check for a known element that indicates the app is running
            # e.g., check for 'stApp' class which is common in Streamlit apps
            try:
                driver.find_element(By.CLASS_NAME, "stApp")
                logger.info("Confirmed: Streamlit app container found")
            except:
                logger.warning("Could not confirm app is fully loaded, but wake button was absent")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise e
    finally:
        if driver:
            driver.quit()
            logger.info("Browser session closed")

if __name__ == "__main__":
    check_and_wake_app()
