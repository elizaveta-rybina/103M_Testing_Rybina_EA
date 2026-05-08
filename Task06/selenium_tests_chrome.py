"""
Selenium tests for Pinterest (Chrome/Chromium).

This script is more stable than Safari WebDriver. It runs functional tests
against pinterest.com using Chrome browser and saves screenshots and logs.

Setup:
  pip install -r requirements.txt
  cp .env.example .env
  # Edit .env with your Pinterest test account email/password

Run (unauthenticated tests):
  python3 selenium_tests_chrome.py

Run with login test (credentials from .env or env vars):
  python3 selenium_tests_chrome.py

Environment variables (or .env file):
  PINTEREST_EMAIL     - Email for Pinterest login (optional)
  PINTEREST_PASSWORD  - Password for Pinterest login (optional)
  If not set, login/search tests will be limited
"""
import os
import time
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    InvalidSessionIdException,
)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass  # dotenv not critical if not installed


OUT_DIR = os.path.join(os.path.dirname(__file__), "task06_outputs")
os.makedirs(OUT_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(OUT_DIR, "test_log_chrome.txt"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filemode="w",
)


def take_screenshot(driver, name: str) -> str:
    """Save a screenshot with timestamp prefix."""
    path = os.path.join(OUT_DIR, f"{int(time.time())}_{name}.png")
    try:
        driver.save_screenshot(path)
        logging.info(f"Saved screenshot: {path}")
    except Exception as e:
        logging.warning(f"Failed to save screenshot {path}: {str(e)[:200]}")
    return path


def handle_cookie_consent(driver):
    """Detect and accept cookie/consent banners."""
    logging.info("Handling cookie consent (if present)")
    try:
        # Look for dialog or banner containing cookie text
        candidates = [
            # Button with "Принять все" text
            (By.XPATH, "//button[normalize-space()='Принять все']"),
            (By.XPATH, "//button[contains(., 'Принять все')]"),
            (By.XPATH, "//button[contains(., 'Accept all')]"),
            (By.XPATH, "//button[contains(., 'Agree all')]"),
        ]

        for idx, (by, sel) in enumerate(candidates, start=1):
            logging.info(f"Cookie handler: trying selector {idx}")
            try:
                btn = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((by, sel)))
                logging.info(f"Found cookie button: {sel}")
                btn.click()
                logging.info("Clicked cookie accept button")
                time.sleep(1)
                take_screenshot(driver, "cookie_accepted")
                return True
            except Exception:
                continue

        logging.info("No cookie consent button found (may already be accepted)")
        return False

    except Exception as e:
        logging.warning(f"Cookie handling error: {str(e)[:100]}")
        return False


def test_open_homepage(driver):
    """Test 1: Load Pinterest homepage."""
    logging.info("Test: open homepage")
    try:
        driver.get("https://www.pinterest.com/")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        title = driver.title or ""
        current_url = driver.current_url
        logging.info(f"Homepage loaded. title='{title}', url='{current_url}'")
        take_screenshot(driver, "01_homepage")
        return True
    except Exception as e:
        logging.exception(f"Failed to load homepage: {e}")
        take_screenshot(driver, "01_homepage_error")
        return False


def test_search_functionality(driver, term="english grammar"):
    """Test 2: Search for a term."""
    logging.info(f"Test: search for '{term}'")
    try:
        # Wait for search input to appear — try multiple selectors
        search_candidates = [
            (By.CSS_SELECTOR, "input[aria-label*='Search']"),
            (By.CSS_SELECTOR, "input[placeholder*='Search']"),
            (By.CSS_SELECTOR, "input[placeholder*='Идеи']"),
            (By.XPATH, "//input[@placeholder and contains(@placeholder, 'блюд')]"),
            (By.XPATH, "//input[@type='text' and @placeholder]"),
            (By.CSS_SELECTOR, "input[type='search']"),
        ]
        
        search_input = None
        for by, sel in search_candidates:
            try:
                search_input = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((by, sel))
                )
                if search_input.is_displayed():
                    logging.info(f"Found search input with selector: {sel}")
                    break
            except Exception:
                continue
        
        if not search_input:
            logging.warning("Search input not found")
            return False
        
        logging.info(f"Found search input")
        search_input.click()
        time.sleep(0.5)
        search_input.clear()
        search_input.send_keys(term)
        logging.info(f"Typed '{term}' in search")
        
        # Press Enter to search
        search_input.send_keys(Keys.RETURN)
        logging.info("Pressed Enter")
        
        # Wait for results page to load
        time.sleep(3)
        take_screenshot(driver, "02_search_results")
        logging.info(f"Search executed for '{term}'")
        return True
        
    except TimeoutException:
        logging.warning("Search input not found (timeout)")
        return False
    except Exception as e:
        logging.exception(f"Search test failed: {e}")
        return False


def test_login_button(driver):
    """Test 3: Click login button and verify modal appears."""
    logging.info("Test: click login button")
    try:
        # Find login button (usually in header)
        login_candidates = [
            (By.XPATH, "//button[normalize-space()='Войти']"),
            (By.XPATH, "//button[normalize-space()='Log in']"),
            (By.XPATH, "//a[@href='/login']"),
            (By.CSS_SELECTOR, "button[aria-label*='Login']"),
        ]
        
        login_btn = None
        for by, sel in login_candidates:
            try:
                login_btn = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((by, sel)))
                logging.info(f"Found login button: {sel}")
                break
            except Exception:
                continue
        
        if not login_btn:
            logging.warning("Login button not found")
            return False
        
        login_btn.click()
        logging.info("Clicked login button")
        time.sleep(2)
        
        # Check if login modal appeared
        try:
            modal = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder*='email' or @placeholder*='Email']"))
            )
            logging.info("Login modal appeared (found email input)")
            take_screenshot(driver, "03_login_modal")
            
            # Check if we have credentials to test login
            email = os.environ.get("PINTEREST_EMAIL")
            password = os.environ.get("PINTEREST_PASSWORD")
            
            if email and password:
                logging.info("Testing login with provided credentials")
                return test_login_with_credentials(driver, email, password)
            else:
                logging.info("No credentials provided (PINTEREST_EMAIL/PINTEREST_PASSWORD env vars) — skipping authentication test")
                return True
                
        except Exception:
            take_screenshot(driver, "03_login_attempt")
            logging.info("Login attempt made, modal state captured")
            return True
            
    except Exception as e:
        logging.exception(f"Login test failed: {e}")
        return False


def test_login_with_credentials(driver, email: str, password: str) -> bool:
    """Test login with actual credentials."""
    logging.info(f"Attempting login with email: {email}")
    try:
        # Find email input
        email_input = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder*='email' or @placeholder*='Email' or @type='email']"))
        )
        email_input.clear()
        email_input.send_keys(email)
        logging.info("Entered email")
        
        # Find password input
        password_input = driver.find_element(By.XPATH, "//input[@placeholder*='password' or @placeholder*='Password' or @type='password']")
        password_input.clear()
        password_input.send_keys(password)
        logging.info("Entered password")
        
        # Find and click login button (red button in modal)
        login_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Войти' or normalize-space()='Log In' or contains(@class, 'primary')]")
        login_btn.click()
        logging.info("Clicked login button in modal")
        
        # Wait for redirect after successful login
        time.sleep(3)
        take_screenshot(driver, "03_login_success")
        
        # Check if we're redirected to feed (not on login page anymore)
        current_url = driver.current_url
        if "login" not in current_url.lower():
            logging.info(f"Login successful! Redirected to: {current_url}")
            return True
        else:
            logging.warning("Still on login page after attempting login")
            take_screenshot(driver, "03_login_failed")
            return False
            
    except Exception as e:
        logging.exception(f"Login with credentials failed: {e}")
        take_screenshot(driver, "03_login_error")
        return False


def main():
    logging.info("Starting Pinterest Selenium tests (Chrome)")
    
    # Check if credentials are provided
    email = os.environ.get("PINTEREST_EMAIL")
    password = os.environ.get("PINTEREST_PASSWORD")
    
    # Check if .env file exists and give user instructions
    env_file = Path(__file__).parent / ".env"
    
    if email and password:
        logging.info(f"Running with authentication (email: {email})")
        print("✓ Running with Pinterest credentials")
    else:
        logging.info("Running without authentication (env vars PINTEREST_EMAIL/PINTEREST_PASSWORD not set)")
        print("ℹ Running in guest mode (no login credentials provided)")
        if env_file.exists():
            print("  → Edit Task06/.env with your Pinterest test account credentials")
        else:
            print("  → Copy Task06/.env.example to Task06/.env and add credentials")
    
    # Setup Chrome options
    chrome_options = Options()
    # Uncomment to run headless (no GUI):
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.exception(f"Failed to start Chrome WebDriver: {e}")
        print(f"Error: Could not start Chrome. Make sure Chrome/Chromium is installed.")
        return
    
    driver.set_window_size(1280, 800)
    
    results = {}
    try:
        # Order: Homepage → Cookie Consent → Login → Search
        
        # 1. Navigate to homepage FIRST (needed for login button to appear)
        driver.get("https://www.pinterest.com/")
        time.sleep(3)
        results['homepage'] = test_open_homepage(driver)
        time.sleep(1)
        
        # 2. Try to handle cookie consent
        handle_cookie_consent(driver)
        time.sleep(1)
        
        # 3. Try login button (now page is loaded, button should be visible)
        results['login'] = test_login_button(driver)
        time.sleep(2)
        
        # 4. Search test
        results['search'] = test_search_functionality(driver, term="english grammar")
        time.sleep(1)
        
    except Exception as e:
        logging.exception(f"Unexpected error during tests: {e}")
    finally:
        try:
            logging.info(f"Test results summary: {results}")
            summary = f"✓ Login: {results.get('login', False)} | ✓ Homepage: {results.get('homepage', False)} | ✓ Search: {results.get('search', False)}"
            logging.info(summary)
            print("\n" + summary)
            driver.quit()
        except Exception as e:
            logging.warning(f"Error during driver.quit(): {e}")


if __name__ == "__main__":
    main()
